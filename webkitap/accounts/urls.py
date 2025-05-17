from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.models import User

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Bildirimler
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),
    
    # Tema değiştirme
    path('theme-switch/', views.theme_switch, name='theme_switch'),
] 