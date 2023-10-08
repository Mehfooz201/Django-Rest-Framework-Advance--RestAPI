from decimal import Decimal
from rest_framework import serializers
from store.models import Product, Collection


#Define Serializers, Convert complete data types into JSON here using serializres

class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title']
    


class ProductSerializers(serializers.ModelSerializer): #ModelSerializers
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    # collection = CollectionSerializers()
    collection = serializers.StringRelatedField()
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')


    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    # price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = CollectionSerializers()

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance

