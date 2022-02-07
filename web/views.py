from django.shortcuts import render,redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
def home(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['Your_Email_address']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['kiptoorotiche@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request,"main/index.html",{'form':form})

def about(request):
    return render(request,"main/about_us.html")

def clients(request):
    return render(request,"main/our_clients.html")


def our_service(request):
    return render(request,"main/our_service.html")


def our_partners(request):
    return render(request,"main/our_partners.html")

def service_charter(request):
    return render(request,"main/service_charter.html")

def gallery(request):
    return render(request,"main/gallery.html")

def successView(request):
    return HttpResponse('Success! Thank you for your message.')