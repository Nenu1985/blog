from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, CreateView
from django.views import View
from .models import Post, Blog, NewsPost
from .forms import PostCreateForm
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

User = get_user_model()


# Create your views here.
# http://127.0.0.1:8000/blog/
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3

    template_name = 'blog/list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('blog:post-list')
    context_object_name = 'post_form'
    form_class = PostCreateForm

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.blog = self.request.user.blog
        new_item.save()
        messages.success(self.request, f'Post added successfully to {new_item.blog}')

        return super().form_valid(form)


class UsersView(ListView):
    model = User
    context_object_name = 'users'


class SubscribeBlogView(View):
    @staticmethod
    def get(request, blog_id):
        blog_to_subscribe = get_object_or_404(Blog, id=blog_id)
        current_blog = request.user.blog
        with transaction.atomic():
            if blog_to_subscribe.user not in current_blog.subscribes.all():
                current_blog.subscribes.add(blog_to_subscribe.user)
                for post in blog_to_subscribe.posts.all():
                    news = NewsPost(blog=blog_to_subscribe, post=post)
                    news.save()
                    current_blog.news_feed.add(news)

        # messages.success(request, f'You have been subscribed to {blog_to_subscribe.user.username}')
        return redirect('blog:post-list')


class UnsubscribeBlogView(View):
    @staticmethod
    def get(request, blog_id):
        blog_to_unsubscribe = get_object_or_404(Blog, id=blog_id)
        current_blog = request.user.blog
        with transaction.atomic():
            if blog_to_unsubscribe.user in current_blog.subscribes.all():
                current_blog.subscribes.remove(blog_to_unsubscribe.user)  # delete subscribes
                current_blog.news_feed.filter(post__blog=blog_to_unsubscribe).delete()  # clean news_feed
        # messages.warning(request, f'You have been unsubscribed from {blog_to_unsubscribe.user.username}')
        return redirect('blog:post-list')


class MarkNewsAsReadView(UpdateView):
    model = NewsPost
    fields = ['read']
    success_url = reverse_lazy('blog:post-list')


class NewsPostDetailView(DetailView):
    model = NewsPost


class TestUserAuthentificate(View):
    @staticmethod
    def get(request):
        user = authenticate(username='vasya', password='1234')
        login(request, user)
        return redirect('blog:post-list')