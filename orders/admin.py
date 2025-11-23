from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('item_name', 'unit_price', 'quantity', 'total_price')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('user', 'total_sum', 'status', 'created_at')
    readonly_fields = ('status', 'created_at')
    inlines = (OrderItemAdmin,)
