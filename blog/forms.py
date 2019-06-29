from django import forms
from .models import Post
from django.utils.text import slugify
from django.utils import timezone

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status')

    def clean(self):
        is_same_post_exists = Post.objects.filter(slug=slugify(self.cleaned_data['title']),
                                               publish__year=timezone.now().year,
                                               publish__month=timezone.now().month,
                                               publish__day=timezone.now().day,
                                               status=self.cleaned_data['status'],
                                               )
        if is_same_post_exists:
            raise forms.ValidationError('A post with the same parameters '
                                        'already exists in the database. Please '
                                        'change the title !')



    def save(self, force_insert=False,
             force_update=False,
             commit=True):
        post = super(PostCreateForm, self).save(commit=False)

        # image_url = self.cleaned_data['url']

        if commit:
            post.save()
        return post
