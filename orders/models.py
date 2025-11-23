from django.db import models

from products.models import Cart, Item
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = ("Order")

    def __str__(self):
        return f'Заказ #{self.id}'
    
    @classmethod
    def create_from_cart(cls, cart):
        order = cls.objects.create(
            user=cart.user,
            status=cls.PAID,
            total_sum=cart.subtotal
        )
        
        for item in cart.items_qs:
            OrderItem.objects.create(
                order=order,
                item_name=item.item,
                unit_price=item.unit_price,
                quantity=item.quantity,
                total_price=item.line_total
            )
        cart.status = Cart.STATUS_CANCELED
        cart.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, null=True, blank='True', decimal_places=2)

    def __str__(self):
        return f'{self.item_name} x {self.quantity}'
