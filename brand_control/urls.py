from django.urls import path, include 
from rest_framework import routers
from brand_control import views
from rest_framework.routers import DefaultRouter
router = routers.DefaultRouter()
# Mantener rutas existentes
router.register(r'Product', views.ProductSerializerView, basename='Product')
router.register(r'category', views.CategorySerializerView, basename='category')
router.register(r'Order', views.OrderSerializerView, basename='Order')
router.register(r'OrderDetails', views.OrderDetailsSerializerView, basename='OrderDetails')
router.register(r'shoppcart', views.ShoppCartSerializerView, basename='shoppcart') 
router.register(r'shoppcartdetails', views.ShoppCartDetailsSerializerView, basename='shoppcartdetails') 
router.register(r'Reviews', views.ReviewsSerializerView, basename='Reviews')

# Nuevos endpoints bajo /api/branding/
from .views import (
    ServiceCategoryViewSet, ServiceViewSet, QuoteRequestViewSet, ProjectViewSet,
    ProjectMessageViewSet, PaymentViewSet
)

branding_router = DefaultRouter()
branding_router.register(r'service-categories', ServiceCategoryViewSet, basename='service-categories')
branding_router.register(r'services', ServiceViewSet, basename='services')
branding_router.register(r'quotes', QuoteRequestViewSet, basename='quotes')
# Importante: registrar 'projects/messages' ANTES que 'projects' para evitar colisiones de rutas
branding_router.register(r'projects/messages', ProjectMessageViewSet, basename='project-messages')
branding_router.register(r'projects', ProjectViewSet, basename='projects')
branding_router.register(r'payments', PaymentViewSet, basename='payments')


urlpatterns = [
    path('brand_control/model/', include(router.urls)),
    path('branding/', include((branding_router.urls, 'branding'))),
]