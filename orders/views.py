import stripe
from django.conf import settings
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.views.generic.base import TemplateView

from orders.models import Order
from products.models import Cart, Item


stripe.api_key = settings.STRIPE_SECRET_KEY


@require_GET
def checkout_page(request):
    csrf = get_token(request)
    cart = Cart.objects.filter(user=request.user, status=Cart.STATUS_OPEN).first()
    if not cart or cart.total_quantity == 0:
        return redirect('products:cart_detail')
    items = []
    for cart_item in cart.items_qs:
        items.append({
            'name': cart_item.item.name,
            'quantity': cart_item.quantity,
            'price': cart_item.unit_price,
            'subtotal': cart_item.line_total,
            'image': getattr(cart_item.item, 'image', None) and cart_item.item.image.url or '' 
        })
    return render(request, 'orders/checkout.html', {
        'title': 'Страница оплаты',
        'public_key': settings.STRIPE_PUBLIC_KEY,
        'csrf_token_value': csrf,
        'success_url': request.build_absolute_uri(reverse('orders:payment_success')),
        'items': items,
    })



@require_POST
def create_payment_intent(request):
    cart = Cart.objects.filter(user=request.user, status=Cart.STATUS_OPEN).first()
    if not cart or cart.total_quantity == 0:
        return JsonResponse({'error': 'Корзина пуста'}, status=400)
    
    intent = stripe.PaymentIntent.create(
        amount=int(cart.subtotal * 100),
        currency='rub',
        automatic_payment_methods={'enabled': True},
    )
    return JsonResponse({
        'clientSecret': intent.client_secret,
        'amount': int(cart.subtotal * 100),
        'currency': 'rub'
    })


@require_GET
def payment_success(request):
    cart = Cart.objects.filter(user=request.user, status=Cart.STATUS_OPEN).first()
    Order.create_from_cart(cart)
    return render(request, 'orders/success.html', {
        'title': 'Спасибо за покупку',
        'public_key': settings.STRIPE_PUBLIC_KEY
    })
