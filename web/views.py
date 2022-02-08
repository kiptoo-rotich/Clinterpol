import json

import requests
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth

from .forms import ContactForm,Payment_Form
from .models import MpesaPayment
from .mpesa_credentials import LipanaMpesaPpassword, MpesaAccessToken


# Create your views here.
def home(request):
    if request.method=="POST":
        transaction_number=request.POST.get('phone_number')
        cell= str(254)+str(int(transaction_number))
        remiting_number=int(cell)
        amount=request.POST.get('pay')
        print("Post")
        form= Payment_Form(request.POST)
        if form.is_valid():
            print("Valid")
            amount= form.cleaned_data.get("amount")
            Payment_reason= form.cleaned_data.get("Payment_reason")
            phone_number= form.cleaned_data.get("phone_number")
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
            headers = {"Authorization": "Bearer %s" % access_token}
            request = {
                "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
                "Password": LipanaMpesaPpassword.decode_password,
                "Timestamp": LipanaMpesaPpassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": remiting_number, 
                "PartyB": LipanaMpesaPpassword.Business_short_code,
                "PhoneNumber": remiting_number, 
                "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
                "AccountReference": "Clinterpol Security and Forensic Consulting Limited",
                "TransactionDesc": "Clinterpol Payments"
            }

            response = requests.post(api_url, json=request, headers=headers)
            return HttpResponse(f'Kindly check your phone {remiting_number} and enter mpesa pin to succesfully pay fare')
    else:
        form= Payment_Form()
    return render(request,"main/index.html",{'form':form})

def about(request):
    return render(request,"main/about_us.html")

def clients(request):
    return render(request,"main/our_clients.html")


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

def successView(request):
    return HttpResponse('Success! Thank you for your message.')
    

def getAccessToken(request):
    consumer_key = 'CHrYGbGBVAqyzI35W84USB9ro8T9m22r'
    consumer_secret = 'Zv53iyFKaJIS6AJ7'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "http://127.0.0.1:8000/api/v1/c2b/confirmation",
               "ValidationURL": "http://127.0.0.1:8000/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)
@csrf_exempt
def call_back(request):
    pass
@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
