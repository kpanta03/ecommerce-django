from django.shortcuts import render, redirect
from .models import ContactMessage

def contact_us(request):
    if request.method == 'POST':
        # grab each field by its name attribute
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        comment = request.POST.get('comment', '').strip()

        # you can add simple validation here if you like
        if name and email and comment:
            ContactMessage.objects.create(
                name=name,
                email=email,
                address=address,
                comment=comment
            )
            return render(request, 'home/index.html', {
                'sent': True
            })

        # if you get here, something was missing
        return render(request, 'home/index.html', {
            'error': "Please fill in name, email, and comment.",
            'old': request.POST
        })

    # GET
    return render(request, 'home/index.html')
