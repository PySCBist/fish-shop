from django.contrib import admin
from .models import DeliveryAddress, Product, Order, OrderItem, DeliveryDate


class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('address',)
    search_fields = ('address',)


admin.site.register(DeliveryAddress, DeliveryAddressAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description',)
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'customer', 'date', 'delivery_date', 'status', 'transaction_id')
    search_fields = ('customer', 'date',)
    list_filter = ('customer', 'date',)
    ordering = ('date', 'customer',)


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'weight')
    search_fields = ('order',)
    list_filter = ('order',)
    ordering = ('order',)


admin.site.register(OrderItem, OrderItemAdmin)


class DeliveryDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'status')
    search_fields = ('date',)
    ordering = ('-date',)


admin.site.register(DeliveryDate, DeliveryDateAdmin)
