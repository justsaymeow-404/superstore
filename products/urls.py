from django.urls import path

from .views import (CatalogListView, ItemDetailView, cart_add, cart_detail,
                    cart_remove)

app_name = 'products'

urlpatterns = [
    path('', CatalogListView.as_view(), name='index'),
    path('<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('add/', cart_add, name='cart_add'),
    path('cart/remove/', cart_remove, name='cart_remove'),
    path('cart/', cart_detail, name='cart_detail')
]
