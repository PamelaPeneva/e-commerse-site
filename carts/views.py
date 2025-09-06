from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from store.models import Product, Variation

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
    # get the product:
    product = Product.objects.get(id=product_id)

    # get the variations:
    item_variations = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST.get(key)
            if key != 'csrfmiddlewaretoken':
                variation = Variation.objects.get(variation_category__iexact=key, variation_value__iexact=value)
                item_variations.append(variation)

    # Get or create the cart:
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    # get the cart item:
    cart_item = CartItem.objects.filter(cart=cart, product=product)
    # if the cart item already exists:
    if cart_item:
        # check if same variations exist
        ex_var_list = []
        ids = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            ids.append(item.id)

        # if yes increment quantity of existing
        if item_variations in ex_var_list:
            cart_item_to_inc_index = ex_var_list.index(item_variations) # 0
            cart_item_to_inc_id = ids[cart_item_to_inc_index]  # 0, id 27
            cart_item_to_increment = CartItem.objects.get(cart=cart, product=product, id=cart_item_to_inc_id)
            cart_item_to_increment.quantity += 1
            cart_item_to_increment.save()
        else:  # make new cart item
            new_cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
            new_cart_item.save()
            new_cart_item.variations.set(item_variations)

    else: # if the cart item doesnt exist:
        cart_item = CartItem(cart=cart, product=product, quantity=1)
        cart_item.save()
        cart_item.variations.set(item_variations)

    return redirect('cart')

def update_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)

    quantity_change = request.POST.get('quantity_change')
    if quantity_change == '1':
        cart_item.quantity += 1
        cart_item.save()
    elif quantity_change == '-1':
        cart_item.quantity -= 1
        cart_item.save()
        if  cart_item.quantity <= 0:
            cart_item.delete()
    return redirect('cart')

def delete_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
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
