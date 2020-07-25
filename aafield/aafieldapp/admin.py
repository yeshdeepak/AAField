from django.contrib import admin


from .models import Parks,Park_Properties,Property_Status,Reservation,Transaction

class ParkAdmin(admin.ModelAdmin):
    model=Parks
    list_display = ['Park_Name']

class PropertyAdmin(admin.ModelAdmin):
    model=Park_Properties
    list_display = ['Park_Name','Property_Name','Property_Description','Property_Guest_Capacity','Property_Location','Slot','Price']

class PropertyStatusAdmin(admin.ModelAdmin):
    model=Property_Status
    list_display = ['Reservation_ID','Park_Name','Property_Name','Report_TimeDate','Property_Status_Description','Expenses','Maintenance_ID']

class ReservationAdmin(admin.ModelAdmin):
    model=Reservation
    list_display = ['id','Park_Name','Property_Name','Customer_Name','Event_Date','Slot','Team_Size','Status']

class TransactionAdmin(admin.ModelAdmin):
    model=Transaction
    list_display = ['Park_Name','Property_Name']

admin.site.register(Parks,ParkAdmin)
admin.site.register(Park_Properties,PropertyAdmin)
admin.site.register(Property_Status,PropertyStatusAdmin)
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Transaction,TransactionAdmin)


