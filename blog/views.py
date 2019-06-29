from django.shortcuts import render, get_object_or_404, redirect, reverse, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views import View
from .models import Post
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# http://127.0.0.1:8000/blog/
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3

    template_name = 'post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    if request.method == 'POST':
        return HttpResponse("You sent POST query!")
    else:  # GET

        return render(request,
                      'post/detail.html',
                      {'post': post,
                       },
                      )


class PostCreateView(View):
    form_class = PostCreateForm

    template_name = 'post/post_create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'post_form': form})

    # @login_required
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            new_item = form.save(commit=False)
            # assign current user to the item

            new_item.blog = request.user.blog
            new_item.save()
            messages.success(request, f'Post added successfully to {new_item.blog}')
            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
            # return redirect(reverse('blog:post-list'))

        return render(request, self.template_name, {'post_form': form})