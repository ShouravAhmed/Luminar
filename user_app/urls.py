from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('varify_account/', views.varify_account, name='varify_account'),
    path('varify_account_success/<str:pk>/', views.varify_account_success, name='varify_account_success'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='user_app/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='user_app/reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user_app/reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user_app/reset_complete.html'), name='password_reset_complete'),

    path('profile/<str:pk>/update/', views.update_profile, name='update_profile'),
    
    path('skill/create/', views.create_skill, name='create_skill'),
    path('skill/<str:pk>/update/', views.update_skill, name='update_skill'),
    path('skill/<str:pk>/delete/', views.delete_skill, name='delete_skill'),
    
    path('exprience/create/', views.create_exprience, name='create_exprience'),
    path('exprience/<str:pk>/update/', views.update_exprience, name='update_exprience'),
    path('exprience/<str:pk>/delete/', views.delete_exprience, name='delete_exprience'),
    
    path('achivement/create/', views.create_achivement, name='create_achivement'),
    path('achivement/<str:pk>/update/', views.update_achivement, name='update_achivement'),
    path('achivement/<str:pk>/delete/', views.delete_achivement, name='delete_achivement'),
    
    path('project/create/', views.create_project, name='create_project'),
    path('project/<str:pk>/update/', views.update_project, name='update_project'),
    path('project/<str:pk>/delete/', views.delete_project, name='delete_project'),
    
    path('interest/create/', views.create_interest, name='create_interest'),
    path('interest/<str:pk>/update/', views.update_interest, name='update_interest'),
    path('interest/<str:pk>/delete/', views.delete_interest, name='delete_interest'),
]
