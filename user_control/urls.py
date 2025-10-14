from django.urls import path, include
from rest_framework import routers
from user_control import views

app_name = 'user_control'
router = routers.DefaultRouter()
router.register(r'register', views.UserRegisterView, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    # Alias explícito para compatibilidad con tests que invocan 'user_control:register'
    path('register/', views.UserRegisterView.as_view({'post': 'create'}), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('session-status/', views.SessionStatusView.as_view(), name='session-status'),
    path('protected/', views.ProtectedView.as_view(), name='protected'),
    path('admin/create-user/', views.CreateUserByAdminView.as_view(), name='admin-create-user'),
    path('admin/create-branch/', views.CreateBranchByAdminView.as_view(), name='admin-create-branch'),
    path('admin/users/', views.AdminUserListView.as_view(), name='admin-users'),
    path('admin/designers/', views.AdminDesignersListView.as_view(), name='admin-designers'),
    path('admin/set-role/', views.AdminSetRoleView.as_view(), name='admin-set-role'),
    path('users/basic-info/', views.GetUsersBasicInfoView.as_view(), name='users-basic-info'),
    path('check-username/', views.CheckUsernameAvailabilityView.as_view(), name='check-username'),
    path('check-email/', views.CheckEmailAvailabilityView.as_view(), name='check-email'),
    path('test/', views.TestView.as_view(), name='test'),
]
