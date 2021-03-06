from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import CustomUser,Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    model=Profile
    list_display = ['user','address', 'city', 'state', 'is_customer', 'is_employee', 'is_maintenanceperson']



class CustomUserAdmin(UserAdmin):
   add_form = CustomUserCreationForm
   form = CustomUserChangeForm
   model = CustomUser
   list_display = ['username','first_name','last_name','email']

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Profile,ProfileAdmin)
