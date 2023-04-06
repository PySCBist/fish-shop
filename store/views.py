from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, Order


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
