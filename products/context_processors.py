from decimal import Decimal

from products.models import Cart


def cart_context(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status=Cart.STATUS_OPEN).first()
        return {
            'cart': cart,
            'cart_count': cart.total_quantity if cart else 0,
            'cart_total': cart.subtotal if cart else Decimal(0.00)
        }
    return {'cart': None, 'cart_count': 0, 'cart_total': Decimal(0.00)}
