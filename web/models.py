from django.db import models

# Create your models here.
class ContactUs(models.Model):
    First_name=models.CharField(max_length=20)
    Last_name=models.CharField(max_length=20)
    Phone_number=models.IntegerField()
    Your_Email_address=models.EmailField()
    subject=models.CharField(max_length=50)
    message=models.TextField()

