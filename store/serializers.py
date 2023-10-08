from rest_framework import serializers
from . import models


#Define Serializers, Convert complete data types into JSON here using serializres

class ProductSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)