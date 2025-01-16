from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='my-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('final/', views.final_view, name='final'),
    path('approve-user/<int:user_id>/', views.admin_approve_user, name='approve-user'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('reject-user/<int:user_id>/', views.reject_user, name='reject-user'),
]
