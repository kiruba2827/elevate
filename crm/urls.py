from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='my-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('final/', views.final_view, name='final'),
]
