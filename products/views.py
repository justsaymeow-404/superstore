import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from .models import Cart, Item

stripe.api_key = settings.STRIPE_SECRET_KEY



class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'SuperShop'


class ItemDetailView(TitleMixin, DetailView):
    model = Item
    template_name = 'products/item_detail.html'
    title = 'Страница товара'
    context_object_name = 'item'


class CatalogListView(TitleMixin, ListView):
    model = Item
    template_name = 'products/catalog.html'
    title = 'Каталог'



@require_POST
@login_required
def cart_add(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, status=Cart.STATUS_OPEN)
    item = Item.objects.filter(id=int(request.POST.get('product_id'))).first()
    cart.add_item(item)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@require_POST
@login_required
def cart_remove(request):
    cart = Cart.objects.filter(user=request.user, status=Cart.STATUS_OPEN).first()
    item = Item.objects.filter(id=int(request.POST.get('product_id'))).first()
    cart.remove_item(item)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user, status=Cart.STATUS_OPEN)
    if cart.exists():
        return render(request, 'products/cart.html', {'items': cart.first().items_qs, 'title': 'Корзина'})
    return render(request, 'products/cart.html', {'title': 'Корзина'})



