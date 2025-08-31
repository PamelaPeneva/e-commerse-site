from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from .models import Product


"""
this view is used for 2 things:
listing all products  http://127.0.0.1:8000/store/
and listing all products from a category  http://127.0.0.1:8000/store/jeans
"""
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.filter(is_available=True)
        products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count
    }
    return render(request, 'store.html', context)

# http://127.0.0.1:8000/store/some-slug/some-slug
def product_detail(request, category_slug, item_slug):
    # category = get_object_or_404(Category, slug=category_slug)
    # product = get_object_or_404(Product, slug=item_slug, category=category)
    product = Product.objects.get(slug=item_slug, category__slug=category_slug)

    # if i item is already in cart dont show add to cart button
    cart = _cart_id(request)
    in_cart = CartItem.objects.filter(product=product, cart__cart_id=cart).exists()  # T/F
    # return HttpResponse(in_cart)
    # exit()

    context = {
        'product': product,
        'in_cart': in_cart,
    }
    return render(request, 'product-detail.html', context)