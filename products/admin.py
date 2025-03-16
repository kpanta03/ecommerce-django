from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Category)

#Inline class for ProductImage
class ProductImageAdmin(admin.StackedInline):
    model =ProductImage

#  Admin class for Product model
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

# Register the Product model with its custom admin. add product garda add image pani tei awos vanera yesto gareko.
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
