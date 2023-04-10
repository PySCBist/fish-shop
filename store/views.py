import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import Product, Order, OrderItem, DeliveryDate


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
        items = Order.objects.get(customer__username=user,
                                  status='not formed').get_total_items
        return JsonResponse({'count': items})


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
