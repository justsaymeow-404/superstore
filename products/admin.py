from django.contrib import admin

from products.models import Cart, CartItem, Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'rating', ('price', 'quantity'), 'image',)
    search_fields = ('name', )


class CartItemAdmin(admin.TabularInline):
    model = CartItem
    fields = ('item', 'quantity', 'unit_price')
    search_fields = ('item', )
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    fields = ('user', 'created_at', 'status')
    readonly_fields = ('created_at',)
    search_fields = ('user', )
    inlines = (CartItemAdmin, )
