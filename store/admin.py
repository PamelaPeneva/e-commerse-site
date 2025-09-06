from .import models

from django.contrib import admin

@admin.register(models.Product)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

@admin.register(models.Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product__product_name', 'variation_category', 'variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product__product_name', 'variation_category', 'variation_value')
