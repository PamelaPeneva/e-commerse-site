from django.db import models

from store.models import Product, Variation


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True) # will be storing the sessionID str from cookies
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

# when we add product in cart it becomes cart item
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)

    # user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    variations = models.ManyToManyField(Variation, blank=True)

    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    # def __unicode__(self):
    #     return self.product
