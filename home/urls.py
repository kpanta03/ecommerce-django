from django.urls import path
from home.views import *

urlpatterns = [
    path('' , index , name="index"),
]