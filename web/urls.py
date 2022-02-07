from unicodedata import name
from . import views
from django.urls import path
from .views import successView


urlpatterns=[ 
    path('',views.home,name='Home'),
    path('About_us',views.about,name='About'),
    path('Our_services',views.our_service,name='Services'),  
    path('Our_clients',views.clients,name='Clients'),
    path('Our_partners',views.our_partners,name='Partners'),
    path('Gallery',views.gallery,name='Gallery'),
    path('Service Charter',views.service_charter,name='Charter'),
    path('success/', successView, name='success'),
    ]