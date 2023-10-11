from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collection', views.CollectionViewSet)

router.urls
# URLConf

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls))
    # path('products/', views.ProductViewSet.as_view()),
    #Genetric view expects pk intead of
    # path('products/<int:pk>/', views.ProductDetail.as_view()),

    # path('collection/', views.CollectionList.as_view()),
    # path('collection/<int:id>/', views.collection_detail),
]
