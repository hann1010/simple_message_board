from . import views
from django.urls import path
from .views import (
    Chat_View,
    ChatCreateView,
    ChatUpdateView,
    ChatCommentCreateView,
    ChatDeleteView,
    UserDetailView
    )


urlpatterns = [
    path('', views.home, name='chat-home'),
    path('chat/chat-view/chat_json/', views.jsonChat, name='chat-json'),
    path('chat/chat-view/', Chat_View.as_view(), name='chat-view'),
    path('chat/chat-new/', ChatCreateView.as_view(), name='chat-new'),
    path('chat/<int:pk>/update/', ChatUpdateView.as_view(), name='chat_update'),
    path('chat/<int:pk>/comment/', ChatCommentCreateView.as_view(), name='chat_comment'),
    path('chat/<int:pk>/delete/', ChatDeleteView.as_view(), name='chat_delete'),
    path('chat/<int:pk>/user_info/', UserDetailView.as_view(), name='chat-user_info'),
    ]