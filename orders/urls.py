from django.urls import path

from orders.views import checkout_page, create_payment_intent, payment_success

app_name = 'orders'

urlpatterns = [
    path('checkout/', checkout_page, name='checkout'),
    path('create-payment-intent/', create_payment_intent, name='create_payment_intent'),
    path('success/', payment_success, name='payment_success')
]



