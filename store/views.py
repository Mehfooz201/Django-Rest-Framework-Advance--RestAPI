from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import status

#Django-RestFull
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializers





# Create your views here.
@api_view()
def product_list(request):
    products = Product.objects.all()
    serializers = ProductSerializers(products, many=True)
    return Response(serializers.data)

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializers(product)
    return Response(serializer.data)
    