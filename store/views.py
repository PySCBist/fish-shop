import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from .models import Product, Order, OrderItem, DeliveryDate, DeliveryAddress


class ProductListView(ListView):
    model = Product
    template_name = 'store/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if Order.objects.filter(customer=self.request.user,
                                status='not formed').exists():
            order = Order.objects.get(customer=self.request.user,
                                      status='not formed')
            context['products_ids'] = order.orderitem_set.all()
        return context


class CartCountView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = data['user']
        if Order.objects.filter(customer__username=user,
                                status='not formed').exists():
            items = Order.objects.get(customer__username=user,
                                      status='not formed').get_total_items
        else:
            items = 0
        return JsonResponse({'count': items})


def basket(request):
    addresses = DeliveryAddress.objects.all()
    if request.user.is_authenticated and Order.objects.filter(
            customer=request.user, status='not formed').exists():
        order = Order.objects.get(customer=request.user,
                                  status='not formed')
        if DeliveryDate.objects.filter(status='open').exists():
            order.delivery_date = DeliveryDate.objects.get(status='open')
            order.save()
        items = order.orderitem_set.all()
        addresses = DeliveryAddress.objects.all()
    else:
        items = []
        order = {'get_total_items': 0,
                 'get_total_price': 0,
                 'addresses': addresses}
    return render(request, 'store/basket.html',
                  context={'items': items, 'order': order,
                           'addresses': addresses})


@login_required()
def orders(request):
    orders_qs = Order.objects.exclude(customer=request.user,
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
        if Order.objects.filter(customer=request.user,
                                status='not formed').exists():
            data = json.loads(request.body)
            address_id = data['address']
            address = DeliveryAddress.objects.get(id=address_id)
            order = Order.objects.get(customer=request.user,
                                      status='not formed')
            order.status = 'formed'
            order.address = address
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
        return JsonResponse(f'Successfully payment order {order_id}',
                            safe=False)


def success_payment(request):
    render(request, template_name='store/success_payment.html', context={})
