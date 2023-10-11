from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.ProductList.as_view()),
    #Genetric view expects pk intead of
    path('products/<int:pk>/', views.ProductDetail.as_view()),

    path('collection/', views.CollectionList.as_view()),
    path('collection/<int:id>/', views.collection_detail),
]
