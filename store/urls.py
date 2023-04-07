from django.urls import path

from store import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('basket/', views.basket, name='basket'),
    path('orders/', views.orders, name='orders'),
    path('about/', views.about, name='about'),
    path('update_item/', views.update_item, name='update_item '),
    path('make_order/', views.make_order, name='make_order ')
]
