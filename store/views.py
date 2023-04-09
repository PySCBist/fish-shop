import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import Product, Order, OrderItem, DeliveryDate


class ProductListView(ListView):
    model = Product
    template_name = 'store/index.html'


def basket(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user,
            status='not formed')
        if DeliveryDate.objects.filter(status='open').exists():
            order.delivery_date = DeliveryDate.objects.get(status='open')
            order.save()
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_total_items': 0,
                 'get_total_price': 0}
    return render(request, 'store/basket.html',
                  context={'items': items, 'order': order})


@login_required()
def orders(request):
    order = Order.objects.get(customer=request.user, status='formed')
    items = order.orderitem_set.all()
    return render(request, 'store/orders.html',
                  context={'items': items, 'order': order})


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
        return JsonResponse({"quantity": order_item.quantity,
                             "total_items": order.get_total_items}, status=200)
    return JsonResponse('GET method not allowed', safe=False)


def make_order(request):
    if Order.objects.filter(customer=request.user,
                            status='not formed').exists():
        order = Order.objects.get(customer=request.user,
                                  status='not formed')
        order.status = 'formed'
        order.save()
        return JsonResponse('Order formed')
    return JsonResponse('No products in basket. Order not formed.')
