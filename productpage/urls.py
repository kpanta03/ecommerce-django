from django.urls import path
from productpage.views import product_page

urlpatterns = [
    path('products/' ,product_page , name="products"),
]