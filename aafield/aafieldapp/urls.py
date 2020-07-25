from accounts.views import user_login
from aafieldapp.views import  park_list, search, home,parkview,propertyview,emppropertyview,empparkview,updatepropertyview,updateparkview,deleteparkview,addpropertyview,deletepropertyview,bookpropertyview,assignmaintenanceview,addmaintenanceview,addchargesview,addmaintchargesview, payment, viewbookings,addComments, updateComments,customerBooking, cancelBooking,finalPayment
from django.urls import path, re_path
from django.conf.urls import url

from . import views
from .import tables

app_name = 'aafieldapp'

urlpatterns = [
   path('',park_list, name='park_list'),
   path('search', search, name='search'),
   path('park/<id>', parkview, name='parkview'),
    path('employeepark/<id>', empparkview, name='employeeparkview'),
    path('property/<id>/<pid>', propertyview, name='propertyview'),
   path('employeeproperty/<id>', emppropertyview, name='emppropertyview'),
    path('updatepark/<id>', updateparkview, name='updatepark'),
    path('addpark', updateparkview, name='addpark'),
    path('deletepark/<id>', deleteparkview, name='deletepark'),
    path('addproperty/<id>', addpropertyview, name='addproperty'),
    path('updateproperty/<id>', updatepropertyview, name='updateproperty'),
    path('deleteproperty/<id>', deletepropertyview, name='deleteproperty'),
    path('login', user_login, name='login'),
    path('book', bookpropertyview, name='bookproperty'),
    path('maintenance', assignmaintenanceview, name='assignmaintenance'),
    path('maintenance/<id>', addmaintenanceview, name='addmaintenance'),
    path('maintenancecost', addchargesview, name='addcharges'),
    path('maintenancecost/<id>', addmaintchargesview, name='addmaintcharges'),
    path('bookings', viewbookings, name='viewbookings'),

 #path('django.views.static',
                            #(r'^media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}), ),
    re_path(r'^home/$', home, name='home'),
    path('payment', payment, name='payment'),
    path('finalPayment', finalPayment, name='finalPayment'),

 path('addComments/<id>', addComments, name='addComments'),
    path('updateComments', updateComments, name='updateComments'),
    path('customerBooking', customerBooking, name='customerBooking'),
    path('cancelBooking/<id>', cancelBooking, name='cancelBooking'),
]
