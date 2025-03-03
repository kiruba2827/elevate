from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import request_internet_access
from .views import whitelist_ip
from .views import get_system_details
from .views import system_details_page
from .views import check_authentication 

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
    path("add-event/", views.add_event, name="add_event"),
    path('update-users/', views.update_users, name='update-users'),
    path('home1/', views.home1, name='home1'),
    path('home2/', views.home2, name='home2'),
    path('home3/', views.home3, name='home3'),

    path('about-us/', views.about_us, name='about_us'),
    path('our-mission/', views.our_mission, name='our_mission'),
    path('our-team/', views.our_team, name='our_team'),

    path('contact/email/', views.email_us, name='email_us'),
    path('contact/call/', views.call_us, name='call_us'),
    path('contact/visit/', views.visit_us, name='visit_us'),
    path('delete_event/', views.delete_event, name='delete_event'),
     # Services Dropdown
    path('service1/', views.service1, name='service1'),
    path('service2/', views.service2, name='service2'),
    path('service3/', views.service3, name='service3'),
    path('service4/', views.service4, name='service4'),

    # Downloads Dropdown
    path('download1/', views.download1, name='download1'),
    path('download2/', views.download2, name='download2'),
    path('download3/', views.download3, name='download3'),
    path('request-internet-access/', request_internet_access, name='request_internet_access'),
    path('whitelist-ip/', whitelist_ip, name='whitelist_ip'),
    path('api/system-details/', get_system_details, name='system-details'),
    path('system-details/', system_details_page, name='system_details'),
    path('approve-all/', views.approve_all_users, name='approve-all-users'),
     path('auth-status/', check_authentication, name='auth_status'),
]