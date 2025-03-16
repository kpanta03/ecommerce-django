from django.urls import path
from accounts.views import *


urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('signup/' ,signup_page , name="register"),
#    path('activate/<email_token>/' , activate_email , name="activate_email"),
   path('cart/' ,cart , name="cart"),
   path('add_to_cart/<uid>/' ,add_to_cart , name="add_to_cart"),
   path('remove_cart/<uuid:cart_item_uid>/',remove_cart,name="remove_cart"),
    path('update_cart/<uuid:cart_item_uid>/',update_cart, name='update_cart'),
   

]