from .models import Product
from django_filters.rest_framework import FilterSet


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id' : ['exact'],
            'unit_price' : ['gt', 'lt'] #Less than (lt) and greater than (gt) value
        }