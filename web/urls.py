from unicodedata import name
from . import views
from django.urls import path


urlpatterns=[ 
    path('',views.home,name='Home'),
    path('About_us',views.about,name='About'),
    ]