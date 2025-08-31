from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name='store'),  # all products

    path('<slug:category_slug>', views.store, name='products_by_category'),

    path('<slug:category_slug>/<slug:item_slug>', views.product_detail, name='product_detail'),

]