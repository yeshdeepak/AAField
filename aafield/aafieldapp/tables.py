from django_tables2 import tables, TemplateColumn
from aafieldapp.models import Parks

class TrainingTable(tables.Table):
    class Meta:
         model = Parks
         attrs = {'class': 'table table-sm'}
         fields = ['Park_Name', 'Park_Address', 'Property_Attendant_Phone','Details']
         Details = TemplateColumn(template_name='aafieldapp/templates/aafieldapp/park_view.html')