from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect
from products.models import *
from accounts.models import *



# Create your views here.
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        # for email activation
        # if not user_obj[0].profile.is_email_verified:
        #     messages.warning(request, 'Your account is not verified.')
        #     return HttpResponseRedirect(request.path_info)


        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')
        
        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)#jun page bata request ayo auto tei page ma redirect garxa.

    return render(request ,'accounts/login.html')

def signup_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
        
        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        # messages.success(request, 'see your email in mail.')#for email activation.
        messages.success(request, 'Your account has been created.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/signup.html')


def add_to_cart(request,uid):
    product=Product.objects.get(uid=uid)
    user=request.user
    cart,_=Cart.objects.get_or_create(user=user, is_paid=False)

    cart_item=CartItems.objects.create(cart=cart,product=product,)


    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def remove_cart(request,cart_item_uid):
    try:
        cart_item=CartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

        

def cart(request):
    context={'cart':Cart.objects.get(is_paid=False,user=request.user)}
    return render(request,'accounts/cart.html',context)


def update_cart(request, cart_item_uid):
    action = request.POST.get("action")  # Get the action (increase or decrease)
    cart_item = CartItems.objects.get(uid=cart_item_uid)

    if action == "increase":
        cart_item.quantity += 1  # Increase the quantity by 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1  # Decrease the quantity by 1 (but not less than 1)

    cart_item.save()  # Save the updated cart item

    return redirect(request.META.get('HTTP_REFERER', '/'))



# email activation 

# def activate_email(request , email_token):
#     try:
#         user = Profile.objects.get(email_token= email_token)
#         user.is_email_verified = True
#         user.save()
#         return redirect('/')
#     except Exception as e:
#         return HttpResponse('Invalid Email token')