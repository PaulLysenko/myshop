from django.contrib import admin
from apps.cart.models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ['ref_code', 'user', 'total_price', 'finalizing_time']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'price', 'creation_time']


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
