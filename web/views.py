from distutils.command.config import config
import json
from math import ceil
from decouple import Csv, config

# import pywhatkit as py
import base64
import requests
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
from django.views.decorators.csrf import csrf_exempt
# from twilio.twiml.messaging_response import MessagingResponse

from .forms import ContactForm,Payment_Form
from .models import MpesaPayment
from .mpesa_credentials import LipanaMpesaPpassword, MpesaAccessToken

from datetime import datetime
now = datetime.now()
hour=int(now.strftime("%H"))
minute=int(now.strftime("%M"))+2
print(minute)
# Create your views here.
def home(request):
    return render(request,"main/index.html")

def about(request):
    return render(request,"main/about_us.html")

def clients(request):
    return render(request,"main/our_clients.html")

class MpesaC2bCredential:
    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    passkey = config('passkey')
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')

def getAccessToken(request):
    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request):
    if request.method=="POST":
            transaction_number=request.POST.get('phone_number')
            cell= str(254)+str(int(transaction_number))
            remiting_number=int(cell)
            amount=request.POST.get('amount')
            form= Payment_Form(request.POST)
            if form.is_valid():
                access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": remiting_number,  # replace with your phone number to get stk push
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": remiting_number,  # replace with your phone number to get stk push
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Clinterpol",
            "TransactionDesc": "Clinterpol Security and Forensics Consulting Limited"
        }
            response = requests.post(api_url, json=request, headers=headers)
            return HttpResponse(f'Kindly check your phone {remiting_number} and enter mpesa pin to succesfully pay {amount} to Clinterpol Security and Forensics Consulting Limited')
    else:
        form= Payment_Form()
    return render(request,"main/events.html",{'form':form})


def our_service(request):
    return render(request,"main/our_service.html")

def background_check(request):
    return render(request,"main/background_check.html")

def our_partners(request):
    return render(request,"main/our_partners.html")

def service_charter(request):
    return render(request,"main/service_charter.html")

def gallery(request):
    return render(request,"main/gallery.html")

def investigations(request):
    return render(request,"main/investigations.html")

def corporate(request):
    return render(request,"main/corporate.html")

def training(request):
    return render(request,"main/training.html")

def contact_us(request):
    form=ContactForm()
    return render(request,"main/contact_us.html",{'form':form})

def mybase(request):
    form=ContactForm()
    return render(request,"base.html",{'form':form})

def security(request):
    return render(request,"main/security.html")

def international_security(request):
    return render(request,"main/international_security.html")

def successView(request):
    return HttpResponse('Success! Thank you for your message.')
    
# def whatsapp(request):
#     py.sendwhatmsg('+254721481236', 'Hello. I would like to get your services.',hour, minute,30)
#     return HttpResponse('Kindly wait. This may that a while as whatsApp is loading...')
