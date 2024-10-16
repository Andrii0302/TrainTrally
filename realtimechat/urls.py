from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('<username>/', views.get_or_create_chatroom, name='start-chat'),
    path('room/<chatroom_name>/', views.chat_view, name='chatroom'),
]
