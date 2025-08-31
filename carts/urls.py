from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),  # display the cart
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),   # add item to the cart (plus icon)
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),   # remove item from the cart (minus icon)
    path('delete_cart/<int:product_id>/', views.delete_cart, name='delete_cart'),   # delete item from the cart (delete icon)
]