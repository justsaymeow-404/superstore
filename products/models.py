from decimal import Decimal

from django.db import models, transaction
from django.db.models import F, Sum

from users.models import User


class Item(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    description = models.TextField(verbose_name='Описание')
    rating = models.DecimalField(verbose_name='Рейтинг', max_digits=3, decimal_places=2)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    quantity = models.IntegerField(verbose_name='Количество')
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Cart(models.Model):
    STATUS_OPEN = 'open'
    STATUS_CANCELED = 'canceled'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Открыт'),
        (STATUS_CANCELED, 'Закрыт')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username}'
    
    @property
    def total_quantity(self) -> int:
        return self.items.aggregate(s=Sum('quantity'))['s'] or 0
    
    @property
    def subtotal(self) -> Decimal:
        agg = self.items.aggregate(s=Sum(F('quantity') * F('unit_price')))
        return agg['s'] or Decimal('0.00')

    @property
    def items_qs(self):
        return self.items.select_related('item')

    @transaction.atomic
    def add_item(self, item):
        item, _ = self.items.select_for_update().get_or_create(
            cart=self,
            item=item,
            defaults={'quantity': 0, 'unit_price': item.price}
        )
        item.quantity += 1
        item.save()

    def remove_item(self, item):
        self.items.filter(item=item).delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.item.name}'

    @property
    def line_total(self):
        return self.unit_price * self.quantity