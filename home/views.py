from django.shortcuts import render
from products.models import Product

def index(request):
    category_slug = request.GET.get('category')  # Get category slug from request
    filter_type = request.GET.get('filter')
    search_query = request.GET.get('search') 

    # Get all products
    products = Product.objects.all()

    # Apply category filter if a valid slug is provided
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Apply filter type if provided
    if filter_type == "sale":
         products = products.filter(discount__gt=0)
    elif filter_type == "new_arrival":
        products = products.filter(category__slug='new-arrival')
    elif filter_type == "best_seller":
        products = products.order_by('-rating')


    if search_query:
        products = products.filter(product_name__icontains=search_query)

    # Fetch 8 random products after filtering
    products = products.order_by('?')[:8]

    return render(request, "home/index.html", context={'products': products})
