from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DeliveryAddress(models.Model):
    address = models.TextField(max_length=120, blank=False,
                               verbose_name='Адрес доставки')

    class Meta:
        verbose_name = 'Адрес доставки'

    def __str__(self):
        return self.address


class Product(models.Model):
    name = models.CharField(max_length=20, blank=False,
                            verbose_name='Продукт')
    price = models.FloatField(verbose_name='Цена')
    image = models.ImageField(upload_to='store/img/products/', blank=False,
                              verbose_name='Картинка продукта')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS = [
        ('new', 'новый'),
        ('paid', 'оплачен'),
        ('shipped', 'отгружено')
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False,
                                 null=True, verbose_name='Покупатель')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    status = models.CharField(choices=ORDER_STATUS, blank=False,
                              verbose_name='Статус заказа')
    address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL,
                                verbose_name='Адрес доставки заказа')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                blank=False, null=True, verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=False,
                              null=True, verbose_name='Заказ')
    quantity = models.IntegerField(default=0, blank=False, null=True,
                                   verbose_name='Кол-во')

    class Meta:
        verbose_name = 'Позиция заказа'
        constraints = [models.UniqueConstraint(fields=['product', 'order'],
                                               name='unique_orderitem')]
