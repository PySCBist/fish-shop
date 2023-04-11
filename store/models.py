from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime as dt

User = get_user_model()


class DeliveryAddress(models.Model):
    address = models.TextField(max_length=120, blank=False,
                               verbose_name='Адрес доставки')

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return self.address


class DeliveryDate(models.Model):
    DELIVERY_DATE_STATUS = [
        ('open', 'открыта'),
        ('closed', 'закрыта'),
    ]
    date = models.DateField(verbose_name='Дата доставки')
    status = models.CharField(max_length=15, choices=DELIVERY_DATE_STATUS,
                              verbose_name='Статус')

    class Meta:
        verbose_name = 'Дата доставки'
        verbose_name_plural = 'Даты доставки'

    def __str__(self):
        return dt.strftime(dt.combine(self.date, dt.min.time()),
                           "%d.%m.%Y")


class Product(models.Model):
    name = models.CharField(max_length=20, blank=False,
                            verbose_name='Продукт')
    price = models.FloatField(verbose_name='Цена')
    description = models.TextField(max_length=150,
                                   verbose_name='Описание товара',
                                   blank=False)
    image = models.ImageField(upload_to='store/img/products/',
                              blank=False,
                              verbose_name='Картинка продукта')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS = [
        ('not formed', 'не сформирован'),
        ('formed', 'сформирован'),
        ('processed', 'обработан'),
        ('paid', 'оплачен'),
        ('shipped', 'отгружен')
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False,
                                 null=True, verbose_name='Покупатель')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, blank=False,
                              verbose_name='Статус заказа')
    address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL,
                                null=True,
                                verbose_name='Адрес доставки заказа')
    delivery_date = models.ForeignKey(DeliveryDate, on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      verbose_name='Дата доставки')
    transaction_id = models.CharField(max_length=30, verbose_name='Транзакция',
                                      null=True, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)

    @property
    def get_total_price(self):
        items = self.orderitem_set.all()
        return sum([item.get_total for item in items])

    @property
    def get_total_items(self):
        items = self.orderitem_set.all()
        return sum([item.quantity for item in items])


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                blank=False, null=True, verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=False,
                              null=True, verbose_name='Заказ')
    quantity = models.PositiveIntegerField(default=0, blank=False, null=True,
                                           verbose_name='Кол-во (шт.)')
    weight = models.PositiveIntegerField(default=0, blank=False,
                                         verbose_name='Общий вес (грамм)')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'
        constraints = [models.UniqueConstraint(fields=['product', 'order'],
                                               name='unique_orderitem')]

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        return self.product.price * self.weight / 1000
