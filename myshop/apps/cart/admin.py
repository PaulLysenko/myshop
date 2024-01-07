from django.contrib import admin

from apps.cart.models import CartItem, Cart


class CartItemAdmin(admin.ModelAdmin):
    pass


class CartAdmin(admin.ModelAdmin):
    pass


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)