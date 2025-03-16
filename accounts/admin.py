from django.contrib import admin

# Register your models here.
from .models import Profile,Cart,CartItems

admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItems)
