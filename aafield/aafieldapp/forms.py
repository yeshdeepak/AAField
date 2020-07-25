from django import forms
from .models import Parks,Park_Properties

class ParksForm(forms.ModelForm):
    class Meta:
        model=Parks
        fields = ('Park_Name','Park_Address','County','Park_Image')
        labels= {'Park_Name': 'Park Name',
                 'Park_Address': 'Address',
                'County': 'County',
                'Park_Image':'Photo'
                 }

class ParkPropertyForm(forms.ModelForm):
    class Meta:
        model=Park_Properties
        fields = ('Park_Name','Property_Name','Property_Description','Property_Guest_Capacity','Property_Location','Slot','Price','Property_Image')
        labels= {'Park_Name': 'Park Name',
                 'Property_Name':'Property_Name',
                 'Property_Description': 'Description',
                'Property_Guest_Capacity': 'Guest Capacity',
                'Property_Location':'Location',
                 'Slot':'Slot',
                 'Price':'Price',
                  'Property_Image':'photo'
                 }


class ParkPropertyForm1(forms.ModelForm):
    class Meta:
        model=Park_Properties
        fields = ('Park_Name','Property_Name','Property_Description','Property_Guest_Capacity','Property_Location','Slot','Price','Property_Image')
        labels= {'Park_Name': 'Park Name',
                 'Property_Name':'Property_Name',
                 'Property_Description': 'Description',
                'Property_Guest_Capacity': 'Guest Capacity',
                'Property_Location':'Location',
                 'Slot':'Slot',
                 'Price':'Price',
                  'Property_Image':'photo'
                 }

    def __init__(self,Park_Name ,*args, **kwargs):
        super(ParkPropertyForm1, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['Park_Name'].queryset = Parks.objects.filter(Park_Name=Park_Name)

