from . import views
from django.urls import path
from .views import (
    #PostListView,
    AllDetailView,
    ThreadDetailView,
    TopicCreateView,
    CommentCreateView,
    PostUpdateView,
    PostDeleteView,
    UserDetailView
)


urlpatterns = [
    path('', views.home, name='forum-home'),
    path('latest/topics/', views.latest_topics, name='forum-latest_topics'),
    path('latest/comments/', views.latest_comments, name='forum-latest_comments'),
    path('latest/all/', views.latest_all, name='forum-latest_all'),
    path('topic/new/', TopicCreateView.as_view(), name='forum_topic-create'),
    path('all/<int:pk>/comment/new/', CommentCreateView.as_view(), name='forum_comment-create'),
    path('all/<int:pk>/open/', AllDetailView.as_view(), name='forum_open_one_post'),
    path('all/<int:pk>/thread/', ThreadDetailView.as_view(), name='forum_thread'),
    path('all/<int:pk>/update/', PostUpdateView.as_view(), name='forum_all_update'),
    path('all/<int:pk>/delete/', PostDeleteView.as_view(), name='forum_all_delete'),
    path('all/<int:pk>/user_info/', UserDetailView.as_view(), name='forum_user_info'),
    
	
]