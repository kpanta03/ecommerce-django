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
            return redirect('profile')
        
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

        # ────────── ensure the new user has a Profile ──────────
        Profile.objects.create(user=user_obj)

        # messages.success(request, 'see your email in mail.')#for email activation.
        messages.success(request, 'Your account has been created.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/signup.html')



from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    # Renders the profile page only if the user is authenticated.
    return render(request, 'accounts/profile.html')

@login_required
def logout_user(request):
    # Logs out the user and then redirects to the login page.
    logout(request)
    return redirect('login')


@login_required(login_url='login')
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

        
@login_required(login_url='login')
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



#payment functionality

import uuid
import requests
from django.conf import settings
from django.shortcuts import render, redirect
# from .models import Cart, CartItems
import hashlib
import base64  
import hmac


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user, is_paid=False)
    amount = cart.get_cart_total()            # sum of product prices
    tax_amount = 2                           # no tax
    service_charge = 2                        # no extra service charge
    delivery_charge = 10                      # your Rs 10 shipping
    total_amount = amount + tax_amount + service_charge + delivery_charge

    # generate a unique transaction UUID
    transaction_uuid = str(uuid.uuid4())

    # the fields we’ll sign
    signed_field_names = "total_amount,transaction_uuid,product_code"
    # build the message string in **exact** this order
    message = (
        f"total_amount={total_amount},"
        f"transaction_uuid={transaction_uuid},"
        f"product_code={settings.ESEWA_MERCHANT_ID}"
    )
    # compute HMAC‑SHA256 and base64‑encode it
    signature = base64.b64encode(
        hmac.new(
            settings.ESEWA_SECRET_KEY.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
    ).decode()

    context = {
        "esewa_url": settings.ESEWA_BASE_URL,
        "amount": amount,
        "tax_amount": tax_amount,
        "product_service_charge": service_charge,
        "product_delivery_charge": delivery_charge,
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
        "product_code": settings.ESEWA_MERCHANT_ID,
        "success_url": settings.ESEWA_SUCCESS_URL,
        "failure_url": settings.ESEWA_FAIL_URL,
        "signed_field_names": signed_field_names,
        "signature": signature,
    }
    return render(request, "accounts/checkout.html", context)


@login_required
def esewa_confirm(request):
    """
    eSewa will redirect here with GET params: amt, scd, pid, rid.
    We then verify the transaction by POSTing to eSewa’s verify endpoint.
    """
    amt = request.GET.get('amt')
    scd = request.GET.get('scd')
    pid = request.GET.get('pid')
    rid = request.GET.get('rid')  # eSewa’s reference id

    # Build verification payload
    data = {
        'amt': amt,
        'scd': settings.ESEWA_MERCHANT_ID,
        'rid': rid,
        'pid': pid,
    }

    # Call eSewa verify API
    resp = requests.post(settings.ESEWA_VERIFY_URL, data=data)
    # eSewa responds with XML. We check if it contains <response>Success</response>
    if b'<response>Success</response>' in resp.content:
        # mark cart paid
        cart = Cart.objects.get(user=request.user, is_paid=False)
        cart.is_paid = True
        cart.save()
        # Optionally, clear or recreate a new cart for future
        Cart.objects.create(user=request.user, is_paid=False)
        return render(request, 'accounts/payment_success.html', {'rid': rid})
    else:
        # Verification failed
        return redirect('esewa_fail')


@login_required
def esewa_fail(request):
    """
    Payment failed or user cancelled. Show an error message.
    """
    return render(request, 'accounts/payment_failed.html')




# email activation 

# def activate_email(request , email_token):
#     try:
#         user = Profile.objects.get(email_token= email_token)
#         user.is_email_verified = True
#         user.save()
#         return redirect('/')
#     except Exception as e:
#         return HttpResponse('Invalid Email token')