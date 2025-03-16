# from django.dispatch import receiver
# from django.db.models.signals import post_save
# import uuid
# from basic.emails import send_account_activation_email
from django.db import models

from django.contrib.auth.models import User
from basic.models import BaseModel
from products.models import *

class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    profile_image = models.ImageField(upload_to = 'profile')

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid=False,cart__user=self.user).count()

    # for email activation
    # is_email_verified = models.BooleanField(default=False)
    # email_token = models.CharField(max_length=100 , null=True , blank=True)


class Cart(BaseModel):  # Inheriting from BaseModel
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carts")
    is_paid=models.BooleanField(default=False)

    def get_cart_total(self):
        cart_items = self.cart_items.all()  # Use related_name to fetch cart items
        total_price = sum(cart_item.get_product_price() for cart_item in cart_items)
        return total_price
    
class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)  # Add quantity field

    def get_product_price(self):
        return self.product.price * self.quantity
    

    
    

# @receiver(post_save , sender = User)
# def  send_email_token(sender , instance , created , **kwargs):
#     try:
#         if created:
#             email_token = str(uuid.uuid4())
#             Profile.objects.create(user = instance , email_token = email_token)
#             email = instance.email
#             send_account_activation_email(email , email_token)

#     except Exception as e:
#         print(e)





