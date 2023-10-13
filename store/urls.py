from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collection', views.CollectionViewSet)

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')


router.urls
# URLConf

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),

    path('', include(product_router.urls)),
    # path('products/', views.ProductViewSet.as_view()),
    #Genetric view expects pk intead of
    # path('products/<int:pk>/', views.ProductDetail.as_view()),

    # path('collection/', views.CollectionList.as_view()),
    # path('collection/<int:id>/', views.collection_detail),
]
