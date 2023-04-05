from django.shortcuts import render


def index(request):
    return render(request, 'store/index.html', context={})


def basket(request):
    return render(request, 'store/basket.html', context={})


def checkout(request):
    return render(request, 'store/checkout.html', context={})


def about(request):
    return render(request, 'store/about.html', context={})
