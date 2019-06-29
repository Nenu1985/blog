from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post-detail'),
    path('post-create/', views.PostCreateView.as_view(), name='post-create'),
    path('subscribe/<int:blog_id>', views.SubscribeBlogView.as_view(), name='subscribe'),
    path('unsubscribe/<int:blog_id>', views.UnsubscribeBlogView.as_view(), name='unsubscribe'),
    path('users/', views.UsersView.as_view(template_name='post/user_list.html'), name='users'),
]
