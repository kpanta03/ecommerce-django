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

 # New paths for profile and logout functionality
    path('profile/', profile, name="profile"),
    path('logout/', logout_user, name="logout"),

# payment
    path('checkout/', checkout, name='checkout'),
    path('esewa-confirm/', esewa_confirm, name='esewa_confirm'),
    path('esewa-fail/', esewa_fail, name='esewa_fail'),
   

]