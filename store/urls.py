from django.urls import path

from store import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('basket/', views.basket, name='basket'),
    path('checkout/', views.checkout, name='checkout'),
    path('about/', views.about, name='about'),
]
