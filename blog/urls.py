from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post-detail'),
    path('post-create/', views.PostCreateView.as_view(), name='post-create'),
    path('subscribe/<int:blog_id>', views.SubscribeBlog.as_view(), name='subscribe'),
    path('unsubscribe/<int:blog_id>', views.UnsubscribeBlog.as_view(), name='unsubscribe'),
]
