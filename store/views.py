from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import status

#Django-RestFull
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializers





# Create your views here.
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method=='POST':
        serializers = ProductSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        # serializers.validated_data
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)
        
    else:
        products = Product.objects.all()
        serializers = ProductSerializers(products, many=True)
        return Response(serializers.data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializers(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializers(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

