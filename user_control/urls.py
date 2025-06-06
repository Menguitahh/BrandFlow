from django.urls import path, include
from rest_framework import routers
from user_control import views

router = routers.DefaultRouter()
router.register(r'register', views.UserRegisterView, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('admin/create-user/', views.CreateUserByAdminView.as_view(), name='admin-create-user'),
    path('admin/create-branch/', views.CreateBranchByAdminView.as_view(), name='admin-create-branch'),
]
