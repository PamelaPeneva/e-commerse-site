from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),  # display the cart
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),   # add item to the cart
    path('update/<int:product_id>/<int:cart_item_id>/', views.update_cart, name='update_cart'),   # plus/minus icon
    path('delete_cart/<int:product_id>/<int:cart_item_id>/', views.delete_cart, name='delete_cart'),   # delete icon
]