from django.shortcuts import render, get_object_or_404
from rest_framework import status
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend

#Django-RestFull
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, DjangoModelPermissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem
from .serializers import ProductSerializers, CollectionSerializers, ReviewSerializer, CartSerializers, CartItemSerializers, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderSerializers, OrderItemSerializers, CreateOrderSerializers, UpdateOrderSerializers
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermission, ViewCustomerHistoryPermission



#----------------------- Cart & CartItem API ----------------------------------

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    # permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializers(data=request.data,
                                            context = {'user_id' : self.request.user.id}
                                            )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        serializer = OrderSerializers(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializers
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializers
        return OrderSerializers

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id  = Customer.objects.only('id').get(user_id=user.id) 
        Order.objects.filter(customer_id=customer_id)
    



# class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializers

    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]



class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        
        return CartItemSerializers
    
    def get_serializer_context(self):
        return {'cart_id' : self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])




#------------------------------------------------------------------------------



#---------------------- Class based - ViewSets ---------------------------------
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter

    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']


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
    permission_classes = [IsAdminOrReadOnly]

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#Reviews
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer




#Customer
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # permission_classes = [DjangoModelPermissions]
    permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)

        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        












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