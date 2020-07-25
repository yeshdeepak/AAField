# Create your views here.
import email

import braintree
from aafield import settings
from aafieldapp.models import Parks, Property_Status,Park_Properties,Reservation,Profile, Transaction
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from aafieldapp.decorators import employee_required, customer_required, maintenanceperson_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import ParksForm,ParkPropertyForm,ParkPropertyForm1
from accounts.forms import UserLoginForm
from accounts.models import CustomUser
import datetime

braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC_KEY,
    private_key=settings.BRAINTREE_PRIVATE_KEY,
)

@login_required
def home(request):
    current_user = request.user
    if(current_user.is_superuser):
        return render(request, 'aafieldapp/home.html')
    elif(current_user.profile.is_customer):
        parks = Parks.objects.all()
        context = {'parks': parks}
        return render(request, 'aafieldapp/customerhome.html', context)
    elif(current_user.profile.is_employee):
        parks=Parks.objects.all()
        context = {'parks': parks}
        return render(request, 'aafieldapp/employeehome.html',context)
    elif (current_user.profile.is_maintenanceperson):
        property_status = maintenancehome(request)
        return render(request, 'aafieldapp/maintenancepersonhome.html', {'property_status': property_status})

@login_required
@maintenanceperson_required
def maintenancehome(request):
    current_user = request.user
    property_status = Property_Status.objects.select_related('Reservation_ID').filter(Maintenance_ID=current_user.id,Reservation_ID__Status='Assigned Maintenance')
    print(property_status)
    return property_status

def search(request):
    if request.method == 'GET':
        park= request.GET.get('Park')
        County= request.GET.get('Location')
        submitbutton= request.GET.get('submit')
        parks=Parks.objects.all()
        context = {'parks': parks}
        if park is not None and park!="":
            park_list= Parks.objects.filter(Park_Name=park)
            pid = Parks.objects.values_list('id', flat=True).filter(Park_Name=park)
            prop=Park_Properties.objects.filter(Park_Name=pid[0])
            context={'park_list':park_list,'prop':prop}
            return render(request, 'aafieldapp/park_view.html', context)
        elif County is not None and County!="":
            park_list= Parks.objects.filter(County=County)
            context={'park_list':park_list}
            return render(request, 'aafieldapp/park_view.html', context)
        else:
            return render(request, 'aafieldapp/search.html',context)
    else:
        return render(request, 'aafieldapp/search.html',context)

def parkview(request,id):
    park_list=Parks.objects.filter(pk=id)
    pid = Parks.objects.values_list('id', flat=True).filter(pk=id)
    prop = Park_Properties.objects.filter(Park_Name=pid[0])
    context = {'park_list': park_list,'prop':prop}
    return render(request, 'aafieldapp/park_view.html', context)

def propertyview(request,id,pid):
    if request.user.is_authenticated:
        if request.method == 'POST' and 'viewslot' in request.POST:
            event_date = request.POST.get('Event_Date')
            park_name = pid
            property_id = id
            park_id = Parks.objects.values_list('id', flat=True).filter(Park_Name=park_name)
            park_id=park_id[0]
            if event_date is not None and event_date != '':
              unavail_slot=Reservation.objects.values_list('Slot',flat=True).filter(Park_Name=park_id,Property_Name=property_id,Event_Date=event_date, Status__in =('Booked','Assigned Maintenance','Added Comments'))
              slot=['8 am - 10 am','10 am - 12 pm','12 pm - 2 pm','2 pm - 4 pm']
              avail_slot=[]
              unavail_slot = [entry for entry in unavail_slot]
              current_date = datetime.date.today().strftime('%Y-%m-%d')
              current_hour = datetime.datetime.today().hour
              if current_date == event_date and current_hour >= 8 and current_hour < 10:
                  temp_slot = ['8 am - 10 am']
              elif current_date == event_date and current_hour >= 10 and current_hour < 12:
                  temp_slot = ['8 am - 10 am', '10 am - 12 pm']
              elif current_date == event_date and current_hour >= 12 and current_hour < 14:
                  temp_slot = ['8 am - 10 am', '10 am - 12 pm', '12 pm - 2 pm']
              elif current_date == event_date and current_hour >= 14 and current_hour < 16:
                  temp_slot = ['8 am - 10 am', '10 am - 12 pm', '12 pm - 2 pm', '2 pm - 4 pm']
              else:
                  temp_slot = []
              print("slot",temp_slot)
              print("unavail_slot",unavail_slot)
              final_unavail_slot = list(set(unavail_slot) | set(temp_slot))
              print("final_unavail_slot",final_unavail_slot)
              #x = set(slot)
              #y = set(final_unavail_slot)
              avail_slot = [i for i in slot + final_unavail_slot if i not in slot or i not in final_unavail_slot]
              # take difference of two lists
              #avail_slot=[]
              #avail_slot = x.difference(y)
              prop = Park_Properties.objects.get(pk=id)
              park = Parks.objects.get(pk=park_id)
              park_address=request.POST.get('park_address')
              context ={'slot':slot,'prop':prop,'event_date':event_date,'park':park,'unavail_slot':final_unavail_slot,'avail_slot':avail_slot}
              return render(request, "aafieldapp/reserve.html", context)
            else:
                prop = Park_Properties.objects.filter(pk=id)
                reserve = Reservation.objects.all()
                current_date = datetime.date.today().strftime('%Y-%m-%d')
                NextDay_Date = datetime.date.today() + datetime.timedelta(days=1)
                NextDay_Date=NextDay_Date.strftime('%Y-%m-%d')
                current_hour = datetime.datetime.today().hour
                if current_hour < 14:
                    current_date = current_date
                else:
                    current_date = NextDay_Date
                context = {'prop': prop, 'reserve': reserve,'current_date':current_date}
                return render(request, "aafieldapp/property_view.html", context)
        elif request.method == 'POST' and 'reserve' in request.POST:
            park_name = request.POST.get('park_name')
            property_name = request.POST.get('property_name')
            park_address = request.POST.get('park_address')
            event_date = request.POST.get('event_date')
            slot = request.POST.get('slot')
            customer_name = request.user
            reservation=Reservation()
            reservation.Park_Name = Parks.objects.get(Park_Name=park_name.strip())
            park_id = Parks.objects.values_list('id', flat=True).filter(Park_Name=park_name.strip())
            reservation.Property_Name = Park_Properties.objects.get(Property_Name = property_name.strip(), Park_Name = park_id[0])
            reservation.Customer_Name = CustomUser.objects.get(username=customer_name)
            reservation.Event_Date = event_date
            reservation.Slot = slot
            reservation.Status = 'Processing'
            if slot == '8 am - 10 am'or slot=='10 am - 12 pm'or slot=='12 pm - 2 pm'or slot=='2 pm - 4 pm':
                reservation.save()
                reserve_id = reservation.id
                braintree_client_token = braintree.ClientToken.generate()
                context={'braintree_client_token':braintree_client_token, 'reserve_id':reserve_id,'park_name':park_name.strip(),'property_name':property_name.strip(),'park_address':park_address,'event_date':event_date,'slot':slot}
                return render(request, "aafieldapp/checkout.html",context)
            else:
                context = {'slot': slot, 'prop': prop, 'event_date': event_date, 'park': park, 'unavail_slot': unavail_slot, 'avail_slot': avail_slot}
                return render(request, "aafieldapp/reserve.html", context)
        else:
            prop = Park_Properties.objects.filter(pk=id)
            reserve = Reservation.objects.all()
            current_date = datetime.date.today().strftime('%Y-%m-%d')
            NextDay_Date = datetime.date.today() + datetime.timedelta(days=1)
            NextDay_Date = NextDay_Date.strftime('%Y-%m-%d')
            current_hour = datetime.datetime.today().hour
            if current_hour < 16:
                current_date = current_date
            else:
                current_date=NextDay_Date
            context = {'prop': prop, 'reserve': reserve,'current_date':current_date}
            return render(request, "aafieldapp/property_view.html", context)
    else:
        form = UserLoginForm()
        return redirect("/accounts/login/")

@login_required
@employee_required
def emppropertyview(request,id):
    prop=Park_Properties.objects.filter(pk=id)
    context = {'prop': prop}
    return render(request, 'aafieldapp/empproperty_view.html', context)

@login_required
@employee_required
def empparkview(request,id):
    park_list=Parks.objects.filter(pk=id)
    pid = Parks.objects.values_list('id', flat=True).filter(pk=id)
    prop = Park_Properties.objects.filter(Park_Name=pid[0])
    context = {'park_list': park_list,'prop':prop}
    return render(request, 'aafieldapp/emppark_view.html', context)

@login_required
@employee_required
def updateparkview(request,id=0):
    if request.method=="GET":
        if id==0:
          form=ParksForm()
        else:
          parks=Parks.objects.get(pk=id)
          form=ParksForm(instance=parks)
        return render(request, 'aafieldapp/AddPark.html', {'form': form})
    else:
        if id==0:
            form=ParksForm(request.POST)
        else:
            parks=Parks.objects.get(pk=id)
            form=ParksForm(request.POST,instance=parks)
        if form.is_valid():
            form.save()
        else:
            raise Http404
        return redirect('/home')

@login_required
@employee_required
def deleteparkview(request,id=0):
    parks = Parks.objects.get(pk=id)
    parks.delete()
    return redirect('/home')

def park_list(request):
    parks=Parks.objects.all()
    context = {'parks': parks}
    return render(request, 'aafieldapp/park_list.html',context)

@login_required
@employee_required
def updatepropertyview(request,id=0):
    if request.method=="GET":
        if id==0:
          form=ParkPropertyForm()
        else:
          property=Park_Properties.objects.get(pk=id)
          form=ParkPropertyForm(instance=property)
        return render(request, 'aafieldapp/updateproperty.html', {'form': form})
    else:
        if id==0:
            form=ParkPropertyForm(request.POST)
        else:
            property=Park_Properties.objects.get(pk=id)
            form=ParkPropertyForm(request.POST,instance=property)
        if form.is_valid():
            form.save()
        return redirect('/home')

@login_required
@employee_required
def addpropertyview(request,id):
    Park_Name = Parks.objects.values_list('Park_Name', flat=True).filter(pk=id)
    Park_Name=Park_Name[0]
    if request.method=="POST":
        form = ParkPropertyForm1(Park_Name,request.POST)
        if form.is_valid():
            form.save()
        return redirect('/home')
    else:
        form = ParkPropertyForm1(Park_Name)
        return render(request, 'aafieldapp/Addproperty.html', {'form': form})


@login_required
@employee_required
def deletepropertyview(request,id=0):
    property = Park_Properties.objects.get(pk=id)
    property.delete()
    return redirect('/home')

@login_required
@customer_required
def bookpropertyview(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            park_name = request.GET.get('park_name')
            property_name = request.GET.get('property_name')
            return render(request, "aafieldapp/reserve.html")

@login_required
@employee_required
def assignmaintenanceview(request):
    current_date=datetime.date.today()
    reservation=Reservation.objects.filter(Event_Date__lte = current_date, Status__exact='Booked')
    context={'reservation':reservation}
    return render(request, 'aafieldapp/assignmaintenance.html', context)

@login_required
@employee_required
def addmaintenanceview(request,id):
    res=Reservation.objects.get(pk=id)
    profile=Profile.objects.filter(is_maintenanceperson=True)
    context={'res':res,'profile':profile}
    if (request.method=="POST"):
     park_name = request.POST.get('park_name')
     property_name = request.POST.get('property_name')
     res_id=request.POST.get('res_id')
     maint_id=request.POST.get('maint_person')
     prop_status = Property_Status()
     prop_status.Park_Name = Parks.objects.get(Park_Name=park_name.strip())
     park_id = Parks.objects.values_list('id', flat=True).filter(Park_Name=park_name.strip())
     prop_status.Property_Name = Park_Properties.objects.get(Park_Name=park_id[0],Property_Name=property_name.strip())
     prop_status.Reservation_ID = Reservation.objects.get(pk=res_id)
     prop_status.Maintenance_ID = CustomUser.objects.get(username=maint_id)
     if maint_id is not None and maint_id!='':
         prop_status.save()
         Reservation.objects.filter(pk=id).update(Status="Assigned Maintenance")
         emailID = CustomUser.objects.filter(username=maint_id).values_list('email', flat=True)
         emailbody = "You have park(s) that needs maintenance check"
         mail = EmailMessage("Maintenance Check", emailbody, settings.EMAIL_HOST_USER, [emailID])
         mail.send()
         current_date = datetime.date.today()
         reservation = Reservation.objects.filter(Event_Date__lte=current_date, Status__exact='Booked')
         context = {'reservation': reservation}
         return render(request, 'aafieldapp/assignmaintenance.html', context)
     else:
         return render(request, 'aafieldapp/AddMaintenance.html', context)

    return render(request, 'aafieldapp/AddMaintenance.html', context)

@login_required
@employee_required
def addchargesview(request):
    current_date=datetime.date.today()
    reservation=Reservation.objects.filter(Event_Date__lte = current_date, Status__exact='Comments Added')
    context={'reservation':reservation}
    return render(request, 'aafieldapp/viewmaintcomments.html', context)

@login_required
@employee_required
def addmaintchargesview(request,id):
    property_status = Property_Status.objects.get(Reservation_ID=id)
    context={'property_status':property_status}
    expenses = request.POST.get('expenses')
    if expenses is not None and expenses!='':
        Property_Status.objects.filter(Reservation_ID=id).update(Expenses=expenses)
        Reservation.objects.filter(pk=id).update(Status="Charges Added")
        current_date = datetime.date.today()
        reservation = Reservation.objects.filter(Event_Date__lte=current_date, Status__exact='Comments Added')
        context = {'reservation': reservation}
        return render(request, 'aafieldapp/viewmaintcomments.html', context)

    else:
        return render(request, 'aafieldapp/addcharges.html', context)
    return render(request, 'aafieldapp/addcharges.html', context)

@login_required
@customer_required
def payment(request):
    nonce_from_the_client = request.POST.get('payment_method_nonce')
    park_name = request.POST.get('park_name')
    property_name = request.POST.get('property_name')
    reserve_id = request.POST.get('reservation_id')
    event_date =  request.POST.get('event_date')
    park_address = request.POST.get('park_address')
    slot = request.POST.get('slot')
    result = braintree.Customer.create({
        "payment_method_nonce": nonce_from_the_client })
    token_generated = result.customer.payment_methods[0].token
    transaction = Transaction()
    transaction.Park_Name = Parks.objects.get(Park_Name=park_name.strip())
    park_id = Parks.objects.values_list('id', flat=True).filter(Park_Name=park_name.strip())
    transaction.Property_Name = Park_Properties.objects.get(Park_Name=park_id[0],Property_Name=property_name.strip())
    transaction.Transaction_Token = token_generated.strip()
    transaction.Reservation_ID = Reservation.objects.get(pk=reserve_id)
    transaction.save()
    Reservation.objects.filter(pk=reserve_id).update(Status="Booked")
    context = {'reserve_id': reserve_id, 'park_name': park_name, 'property_name': property_name, 'park_address': park_address,
             'event_date':event_date, 'slot': slot}
    emailbody = "Congratulations!.Your booking for " + property_name + " in the park " + park_name + " has been confirmed with booking id " + str(reserve_id)
    mail = EmailMessage("Booking Details", emailbody, settings.EMAIL_HOST_USER, [request.user.email])
    mail.send()
    return render(request, 'aafieldapp/booking_done.html',context)

def finalPayment(request):
    park_name = request.POST.get('park_name')
    property_name = request.POST.get('property_name')
    reserve_id = request.POST.get('res_id')
    expense = request.POST.get('expenses')
    park_id = Parks.objects.values_list('id', flat=True).filter(Park_Name=park_name.strip())
    park_properties = Park_Properties.objects.get(Park_Name=park_id[0],Property_Name=property_name.strip())
    price = park_properties.Price
    total_amount = price + int(expense)
    transactions = Transaction.objects.get(Reservation_ID=reserve_id)
    date = datetime.datetime.now()
    Transaction.objects.filter(Reservation_ID=reserve_id).update(Trans_Amount=total_amount,Trans_Time_Date=date)
    token_generated = transactions.Transaction_Token
    transaction = braintree.Transaction.sale({
        "amount": total_amount,
        "payment_method_token": token_generated
    })
    Reservation.objects.filter(pk=reserve_id).update(Status="Payment Done")
    customerName = list(Reservation.objects.filter(pk=reserve_id).values_list('Customer_Name', flat=True))
    emailID = CustomUser.objects.filter(id__in = customerName).values_list('email', flat=True)
    emailbody = "Your payment for " + property_name + " in the park " + park_name + " is completed."
    mail = EmailMessage("Payment Confirmation", emailbody, settings.EMAIL_HOST_USER, [emailID])
    mail.send()
    return redirect('/home')


@login_required
@maintenanceperson_required
def addComments(request,id):
        property_status = Property_Status.objects.get(pk=id)
        return render(request, 'aafieldapp/addComments.html', {'prop_status':property_status})

@login_required
@maintenanceperson_required
def updateComments(request):
    reserve_id = request.POST.get('res_id')
    comments = request.POST.get('comments')
    date = datetime.datetime.now()
    Property_Status.objects.filter(Reservation_ID=reserve_id).update(Property_Status_Description=comments, Report_TimeDate= date)
    Reservation.objects.filter(pk=reserve_id).update(Status="Comments Added")
    profile=Profile.objects.filter(is_employee=True).values_list('user', flat=True)
    emailID = list(CustomUser.objects.filter(id__in = profile).values_list('email', flat=True))
    emailbody = "You have park(s) that needs to be charged for maintenance"
    mail = EmailMessage("Maintenance Charge", emailbody, settings.EMAIL_HOST_USER, emailID)
    mail.send()
    current_user = request.user
    property_status = Property_Status.objects.select_related('Reservation_ID').filter(Maintenance_ID=current_user.id,Reservation_ID__Status='Assigned Maintenance')
    return render(request, 'aafieldapp/maintenancepersonhome.html', {'property_status': property_status})

@login_required
@employee_required
def viewbookings(request):
    reserve=Reservation.objects.all()
    context={'reserve':reserve}
    return render(request, 'aafieldapp/viewbookings.html', context)

@login_required
@customer_required
def customerBooking(request):
    reserve=Reservation.objects.filter(Customer_Name=request.user)
    context={'reserve':reserve}
    return render(request, 'aafieldapp/viewCustomerbookings.html', context)

@login_required
@customer_required
def cancelBooking(request,id):
    Reservation.objects.filter(pk=id).update(Status="Cancelled")
    reserve=Reservation.objects.filter(Customer_Name=request.user)
    context={'reserve':reserve}
    return render(request, 'aafieldapp/viewCustomerbookings.html', context)