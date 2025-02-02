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
     # Other URL patterns...
    path('check-authentication/', views.check_authentication, name='check-authentication'),
]