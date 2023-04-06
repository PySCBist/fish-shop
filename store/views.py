import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, Order, OrderItem


class ProductListView(ListView):
    model = Product
    template_name = 'store/index.html'


def basket(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user,
            status='new')
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_total_items': 0,
                 'get_total_price': 0}
    return render(request, 'store/basket.html',
                  context={'items': items, 'order': order})


def checkout(request):
    return render(request, 'store/checkout.html', context={})


def about(request):
    return render(request, 'store/about.html', context={})


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=request.user,
                                                 status='new')
    order_item, created = OrderItem.objects.get_or_create(order=order,
                                                          product=product)
    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1

    order_item.save()
    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)
