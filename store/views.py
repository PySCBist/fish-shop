import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from .models import Product, Order, OrderItem, DeliveryDate, DeliveryAddress


class ProductListView(ListView):
    model = Product
    template_name = 'store/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.user.is_authenticated:
            order_items = []
            if Order.objects.filter(customer=self.request.user,
                                    status='not formed').exists():
                order = Order.objects.filter(customer=self.request.user,
                                             status='not formed').order_by(
                    'date')[
                    0]
                order_items = order.orderitem_set.all().values_list(
                    'product_id',
                    flat=True)
            context['order_items'] = order_items
        return context


class CartCountView(View):
    def post(self, request, *args, **kwargs):
        if Order.objects.filter(customer=request.user,
                                status='not formed').exists():
            items = Order.objects.filter(customer=request.user,
                                         status='not formed').order_by('date')[
                0].get_total_items
        else:
            items = 0
        return JsonResponse({'count': items})


def basket(request):
    addresses = DeliveryAddress.objects.all()
    if request.user.is_authenticated and Order.objects.filter(
            customer=request.user, status='not formed').exists():
        order = Order.objects.filter(customer=request.user,
                                     status='not formed').order_by('date')[0]
        items = order.orderitem_set.all()
        addresses = DeliveryAddress.objects.all()
    else:
        items = []
        order = {'get_total_items': 0,
                 'get_total_price': 0,
                 'addresses': addresses}
    dates = DeliveryDate.objects.filter(status='open')
    return render(request, 'store/basket.html',
                  context={'items': items, 'order': order,
                           'addresses': addresses,
                           'dates': dates})


@login_required()
def orders(request):
    orders_qs = Order.objects.filter(customer=request.user).exclude(
        status='not formed')
    return render(request, 'store/orders.html',
                  context={'orders': orders_qs})


def about(request):
    return render(request, 'store/about.html', context={})


def update_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = int(data['productId'])
        action = data['action']
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=request.user,
                                                     status='not formed')
        order_item, created = OrderItem.objects.get_or_create(order=order,
                                                              product=product)
        if action == 'add':
            order_item.quantity += 1
        elif action == 'remove':
            order_item.quantity -= 1
        order_item.save()
        if order_item.quantity <= 0:
            order_item.delete()
        if order.get_total_items == 0:
            order.delete()
            return JsonResponse({"quantity": 0, "total_items": 0}, status=200)
        return JsonResponse({"quantity": order_item.quantity,
                             "total_items": order.get_total_items}, status=200)
    return JsonResponse('GET method not allowed', safe=False)


def make_order(request):
    if request.method == 'POST':
        order = Order.objects.filter(customer=request.user,
                                     status='not formed')
        if order:
            data = json.loads(request.body)
            address_id = data['address']
            date_id = data['date']
            address = DeliveryAddress.objects.get(id=address_id)
            delivery_date = DeliveryDate.objects.get(id=date_id)
            order = order.order_by('date')[0]
            order.status = 'formed'
            order.address = address
            order.delivery_date = delivery_date
            order.date = timezone.now()
            order.save()
            return JsonResponse('Order was formed.', safe=False)
        return JsonResponse('No products in basket. Order not formed.',
                            safe=False)
    return JsonResponse('GET method not allowed', safe=False)


def process_order(request):
    if request.method == 'POST':
        transaction_id = timezone.now().timestamp()
        order_id = json.loads(request.body)['order_id']
        order = Order.objects.get(id=order_id)
        order.transaction_id = transaction_id
        order.status = 'paid'
        order.save()
        return JsonResponse(f'Success', safe=False)


def success_payment(request):
    return render(request, 'store/success_payment.html', context={})


def contacts(request):
    return render(request, 'store/contacts.html', context={})
