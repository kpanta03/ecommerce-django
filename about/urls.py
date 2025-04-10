from django.urls import path
from about.views import *

urlpatterns = [
    path('about/' ,about_page , name="about"),
]