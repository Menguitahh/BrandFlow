from django.urls import path, include 
from rest_framework import routers
from brand_control import views
from rest_framework.routers import DefaultRouter
from .views import (
    ProductSerializerView,
    CategorySerializerView,
    OrderSerializerView,
    OrderDetailsSerializerView,
    Shopp_CartSerializerView,
    Shopp_Cart_DetailsSerializerView,
    ReviewsSerializerView,
)



router = routers.DefaultRouter()
router.register(r'Product', ProductSerializerView, basename='Product')
router.register(r'category', views.CategorySerializerView, basename='category')
router.register(r'Order', views.OrderSerializerView, basename='Order')
router.register(r'OrderDetails', views.OrderDetailsSerializerView, basename='OrderDetails')
router.register(r'shoppcart', views.Shopp_CartSerializerView, basename='shoppcart') 
router.register(r'shoppcartdetails', views.Shopp_Cart_DetailsSerializerView, basename='shoppcartdetails') 
router.register(r'Reviews', views.ReviewsSerializerView, basename='Reviews')


urlpatterns = [
    path('brand_control/model/', include(router.urls)),
    
]