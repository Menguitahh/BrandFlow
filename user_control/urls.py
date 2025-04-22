from django.urls import path, include 
from rest_framework import routers
from user_control import views


router = routers.DefaultRouter()


router.register(r'register', views.UserSerializerView, basename='register')
urlpatterns = [
    path('register/', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]