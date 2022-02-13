from unicodedata import name
from . import views
from django.urls import path
from .views import successView


urlpatterns=[ 
    path('',views.home,name='Home'),
    path('About_us/',views.about,name='About'),
    path('Our_services/',views.our_service,name='Services'),  
    path('Our_clients/',views.clients,name='Clients'),
    path('Our_partners/',views.our_partners,name='Partners'),
    path('background_check/',views.background_check,name='background_check'),
    path('Gallery/',views.gallery,name='Gallery'),
    path('Events/',views.lipa_na_mpesa_online,name='Events'),
    path('Investigations/',views.investigations,name='investigations'),
    path('corporate/',views.corporate,name='corporate'),
    path('security/',views.security,name='security'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('base/',views.mybase,name='base'),
    path('training/',views.training,name='training'),
    path('online/lipa/', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    # path('whatsapp/',views.whatsapp,name='whatsapp'),
    path('international_security/',views.international_security,name='international_security'),
    path('Service Charter',views.service_charter,name='Charter'),
    path('success/', successView, name='success'),
    path('access/token/', views.getAccessToken, name='get_mpesa_access_token'),
    ]