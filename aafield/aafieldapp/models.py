from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Profile
from aafield import settings

class Parks(models.Model):
    Park_Name = models.CharField(max_length=50,blank=False, null=False, default=' ')
    Park_Address = models.CharField(max_length=250, blank=True, null=True, default=' ')
    County = models.CharField(max_length=50, blank=True, null=True, default=' ')
    Park_Image = models.ImageField(default='Images/park2.jpg')

    def __str__(self):
        return self.Park_Name

# Create your models here.
class Park_Properties(models.Model):
    Park_Name = models.ForeignKey(Parks, on_delete=models.CASCADE)
    Property_Name = models.CharField(max_length=50, default=' ', null=True, blank=True)
    Property_Description = models.CharField(max_length=50, default=' ', null=True, blank=True)
    Property_Guest_Capacity = models.IntegerField(blank=True, null=True)
    Location_Choices=[('Indoor' ,'Indoor'),('Outdoor','Outdoor')]
    Property_Location= models.CharField(max_length=50,default='Indoor',choices=Location_Choices)
    Slot= models.CharField(max_length=50, default='2 hours', null=True, blank=True)
    Price = models.IntegerField(blank=True, null=True)
    Property_Image=models.ImageField(default='Images/pool.jpg')

    def __str__(self):
        return self.Property_Name

class Reservation(models.Model):
    Park_Name = models.ForeignKey(Parks, on_delete=models.CASCADE)
    Property_Name = models.ForeignKey(Park_Properties, on_delete=models.CASCADE)
    Customer_Name = models.ForeignKey('accounts.customuser', on_delete=models.CASCADE)
    Event_Date = models.DateField(blank=True, null=True)
    Slot = models.CharField(max_length=50, default=' ', null=True, blank=True)
    Team_Size = models.CharField(max_length=50, default=' ', null=True, blank=True)
    Status = models.CharField(max_length=50, default=' ', null=True, blank=True)

    def __str__(self):
        return self.Property_Name.Property_Name

class Property_Status(models.Model):
    Park_Name = models.ForeignKey(Parks, on_delete=models.CASCADE)
    Property_Name = models.ForeignKey(Park_Properties, on_delete=models.CASCADE)
    Report_TimeDate = models.DateTimeField(blank=True, null=True)
    Property_Status_Description = models.CharField(max_length=50, blank=True, null=True)
    Expenses = models.CharField(max_length=50, default=' ', null=True, blank=True)
    Maintenance_ID = models.ForeignKey('accounts.customuser', on_delete=models.CASCADE)
    Reservation_ID=models.ForeignKey(Reservation,on_delete=models.CASCADE,related_name='reservations')

    def __str__(self):
        return self.Park_Name.Park_Name

class Transaction(models.Model):
    Park_Name = models.ForeignKey(Parks, on_delete=models.CASCADE)
    Property_Name = models.ForeignKey(Park_Properties, on_delete=models.CASCADE)
    Reservation_ID = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    Trans_Amount = models.CharField(max_length=50, default=' ', null=True, blank=True)
    Trans_Time_Date = models.DateTimeField(blank=True, null=True)
    Trans_Type = models.CharField(max_length=50, default=' ', null=True, blank=True)
    Transaction_Token = models.CharField(max_length=50, default=' ', null=True, blank=True)

    def __str__(self):
        return self.Trans_Amount