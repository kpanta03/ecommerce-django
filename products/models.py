from django.db import models

# Create your models here.
from basic.models import BaseModel
from django.utils.text import slugify


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to="catgories", null=True , blank=True)
    slug = models.SlugField(unique=True , null=True , blank=True)

    def save(self , *args , **kwargs):
        self.slug = slugify(self.category_name)
        super(Category ,self).save(*args , **kwargs)

    def __str__(self) -> str:
        return self.category_name
# auto slug banauxa.


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    category = models.ManyToManyField(Category ,related_name="products")
    price = models.IntegerField()
    product_desription = models.TextField()
    slug = models.SlugField(unique=True  , null=True , blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    discount = models.IntegerField(default=0)

    def discounted_price(self):
        """Calculate the price after applying the discount."""
        if not self.discount:  # Handles None or 0 cases
            return self.price
        return self.price - (self.price * self.discount / 100)

    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.product_name)
        super(Product ,self).save(*args , **kwargs)


    def __str__(self) -> str:
        return self.product_name

class ProductImage(BaseModel):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="product_images")
    image =  models.ImageField(upload_to="product")