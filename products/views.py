from django.shortcuts import render
from products.models import Product
from accounts.models import *


def get_product(request , slug):
    try:
        product = Product.objects.get(slug =slug)
        print(product)
        return render(request,'product/product.html' , context = {'product' : product})

    except Exception as e:
        print(e)


        