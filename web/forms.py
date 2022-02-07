from django import forms
from django.core.validators import RegexValidator
from .models import ContactUs

def My_TextField_Validator(self):
    return RegexValidator(r'^[-a-zA-Z0-9. ]+$',
    'Valid Input: Alphanumeric characters, dash, dot, space')

class ContactForm(forms.ModelForm):
    First_name = forms.CharField(max_length=50, min_length=4, required=True,
                           help_text='', label='',
                           validators=[My_TextField_Validator],
                           widget=forms.TextInput(attrs={'class': 'form-control', 
                           'placeholder': 'First name'}))
    
    Last_name = forms.CharField(max_length=50, min_length=4, required=True,
                           help_text='', label='',
                           validators=[My_TextField_Validator],
                           widget=forms.TextInput(attrs={'class': 'form-control', 
                           'placeholder': 'Last name'}))
    Your_Email_address = forms.CharField(max_length=50, min_length=4, required=True,
                           help_text='', label='',
                           validators=[My_TextField_Validator],
                           widget=forms.TextInput(attrs={'class': 'form-control', 
                           'placeholder': 'johndoe@gmail.com'}))     
    Phone_number = forms.CharField(required=True,
                           help_text='', label='',
                           validators=[My_TextField_Validator],
                           widget=forms.TextInput(attrs={'class': 'form-control', 
                           'placeholder': 'Phone number'})) 
    subject = forms.CharField(max_length=50, min_length=4, required=True,
                           help_text='', label='',
                           validators=[My_TextField_Validator],
                           widget=forms.TextInput(attrs={'class': 'form-control', 
                           'placeholder': 'Message title'}))  
    message = forms.CharField(required=True,
                           help_text='', label='',
                           validators=[My_TextField_Validator],
                           widget=forms.Textarea(attrs={'class': 'form-control', 
                           'placeholder': 'My message is ...'})) 
    class Meta:
        model=ContactUs
        fields='__all__'