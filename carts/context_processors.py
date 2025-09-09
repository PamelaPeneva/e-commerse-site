# ensures that cart_quantity is always available in all templates.
from carts.models import Cart, CartItem
from carts.views import _cart_id


def cart_counter(request):
    quantity = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            quantity += cart_item.quantity
    except Cart.DoesNotExist:
            quantity = 0

    return {'cart_quantity': quantity}