from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from store.models import Product

"""
a shopping cart system using sessions to identify each user’s cart
session-based cart (cart linked to a session_key instead of a logged-in user) allows
anonymous users to shop.
"""

# ensure every user has a unique cart_id
# cart_id == sessionid str from cookies
def _cart_id(request):
    cartid = request.session.session_key
    if not cartid:
        cartid = request.session.create()  # start a session
    return cartid

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    # get the cart_id
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:  # create one if None
        cart = Cart(cart_id=_cart_id(request))
        cart.save()

    # when we add product in cart it becomes cart item
    try: # increase quality if there
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:  # create if not
        cart_item = CartItem(cart=cart, product=product, quantity=1)
        cart_item.save()

    # return HttpResponse(cart_item.product.product_name)
    # exit()
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def delete_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        # apply 2 persent tax
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'cart.html', context)
