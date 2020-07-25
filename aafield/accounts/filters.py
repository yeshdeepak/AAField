import django_filters
from django_filters import DateFilter, CharFilter
from .models import *
from aafieldapp.models import Parks

class ParkFilter(django_filters.FilterSet):
	#start_date = DateFilter(field_name="date_created", lookup_expr='gte')

	#Park_Name = CharFilter(field_name='Park_Name', lookup_expr='iexact')
	#county = CharFilter(field_name='County', lookup_expr='iexact')


	class Meta:
		model =Parks
		fields = ('Park_Name','County')
