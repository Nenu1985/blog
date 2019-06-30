from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('subscribe/<int:blog_id>', views.SubscribeBlogView.as_view(), name='subscribe'),
    path('unsubscribe/<int:blog_id>', views.UnsubscribeBlogView.as_view(), name='unsubscribe'),
    path('users/', views.UsersView.as_view(template_name='post/user_list.html'), name='users'),
    path('news-post/<int:pk>/', views.MarkNewsAsReadView.as_view(), name='news-post-update'),
    # path('news-post/<int:pk>/', views.MarkNewsAsReadView.as_view(), name='news-post-detail'),
]
