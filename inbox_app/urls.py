from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:pk>/', views.chatbox, name='chatbox'),
    path('inbox/', views.inbox, name='inbox'),
    path('notification/', views.notification, name='notification'),
    path('notification/mark-all-read/', views.mark_all_read, name='mark_all_read')
]

