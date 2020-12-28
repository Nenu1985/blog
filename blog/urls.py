from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/create/', login_required(views.PostCreateView.as_view()), name='post-create'),
    # path('subscribe/<int:blog_id>', login_required(views.SubscribeBlogView.as_view()), name='subscribe'),
    # path('unsubscribe/<int:blog_id>', login_required(views.UnsubscribeBlogView.as_view()), name='unsubscribe'),
    path('users/', views.UsersView.as_view(template_name='blog/user_list.html'), name='users'),
    # path('news-post/<int:pk>/', views.MarkNewsAsReadView.as_view(), name='news-post-update'),
    path('test-user-login/', views.TestUserAuthentificate.as_view(), name='test-user-login'),

]
