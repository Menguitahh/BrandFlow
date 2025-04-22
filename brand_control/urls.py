from django.urls import path, include 
from rest_framework import routers
from brand_control import views
router = routers.DefaultRouter()
# router.register(r'User', views.UserSerializerView, basename='User')
router.register(r'Product', views.ProductSerializerView, basename='Product')
router.register(r'category', views.CategorySerializerView, basename='category')
router.register(r'Order', views.OrderSerializerView, basename='Order')
router.register(r'OrderDetails', views.OrderDetailsSerializerView, basename='OrderDetails')
# router.register(r'Payment', views.PaymentSerializerView, basename='Payment')
router.register(r'shoppcart', views.ShoppCartSerializerView, basename='shoppcart') 
router.register(r'shoppcartdetails', views.ShoppCartDetailsSerializerView, basename='shoppcartdetails') 
# router.register(r'method_payment', views.method_paymentSerializerView, basename='method_payment')
router.register(r'Reviews', views.ReviewsSerializerView, basename='Reviews')


urlpatterns = [
    path('brand_control/model/', include(router.urls)),
    
]