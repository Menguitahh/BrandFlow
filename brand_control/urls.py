from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from brand_control import views

# Router para endpoints de branding
branding_router = DefaultRouter()
branding_router.register(r'service-categories', views.ServiceCategoryViewSet, basename='service-categories')
branding_router.register(r'services', views.ServiceViewSet, basename='services')
branding_router.register(r'quotes', views.QuoteRequestViewSet, basename='quotes')
branding_router.register(r'projects', views.ProjectViewSet, basename='projects')
branding_router.register(r'payments', views.PaymentViewSet, basename='payments')

# Registrar mensajes de proyecto de forma manual
urlpatterns = [
    path('branding/', include((branding_router.urls, 'branding'))),
    # Rutas anidadas manuales para mensajes
    path('branding/projects/<int:project_pk>/messages/', views.ProjectMessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-messages-list'),
    path('branding/projects/<int:project_pk>/messages/<int:pk>/', views.ProjectMessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='project-messages-detail'),
]