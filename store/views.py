from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from django.db.models.aggregates import Count

#Django-RestFull
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet 

from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Collection
from .serializers import ProductSerializers, CollectionSerializers



#---------------------- Class based - ViewSets ---------------------------------
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destory(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Collection
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializers

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


#-------------------------------------------------------------------------------


#---------------------- Class based Generic View -------------------------------
# class ProductList(ListCreateAPIView):
#     def get_queryset(self):
#         return Product.objects.all()
    
#     def get_serializer_class(self):
#         return ProductSerializers
    
#     def get_serializer_context(self):
#         return {'request': self.request}
    

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers

#     # lookup_field ='id'

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)






#Collection
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializers

# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, id):
#     collection = get_object_or_404(Collection, pk=id)
#     if request.method == 'GET':
#         serializer = CollectionSerializers(collection)
#         return Response(serializer.data)



#-----------------------------------------------------------------------------




#---------------------- Class based API's View -------------------------------

# class ProductList(APIView):
#     def get(self, request):
#         products = Product.objects.select_related('collection').all()
#         serializers = ProductSerializers(products, many=True, context={'request':request})
#         return Response(serializers.data)

#     def post(self, request):
#         serializers = ProductSerializers(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(serializers.data, status=status.HTTP_201_CREATED)
    

# class ProductDetail(APIView):
    
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializers(product)
#         return Response(serializer.data)

#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializers(instance=product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# -------------------- Function Based Api's View ----------------------------------
# Create your views here.
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method=='POST':
#         serializers = ProductSerializers(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         # serializers.validated_data
#         serializers.save()
#         return Response(serializers.data, status=status.HTTP_201_CREATED)
        
#     else:
#         products = Product.objects.all()
#         serializers = ProductSerializers(products, many=True)
#         return Response(serializers.data)


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializers(product)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = ProductSerializers(instance=product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# #Collection
# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method=='POST':
#         serializers = CollectionSerializers(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         # serializers.validated_data
#         serializers.save()
#         return Response(serializers.data, status=status.HTTP_201_CREATED)
    
#     elif request.method=='GET':
#         collection = Collection.objects.annotate(product_count=Count('products')) 
#         serializers = CollectionSerializers(collection, many=True)
#         return Response(serializers.data)



# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, id):
#     collection = get_object_or_404(Collection, pk=id)
#     if request.method == 'GET':
#         serializer = CollectionSerializers(collection)
#         return Response(serializer.data)


#------------------------------------------------------------------------------