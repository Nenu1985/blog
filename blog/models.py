from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import signals
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.sites.models import Site
import asyncio
import logging
from django.contrib.auth.models import User
loop = asyncio.get_event_loop()
# User = get_user_model()

# Create your models here.

# Create your models here.



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset() \
            .filter(status='published')


# class Blog(models.Model):
#     user = models.OneToOneField(User,
#                                 on_delete=models.CASCADE)

#     # users_subscribe = models.ForeignKey(User,
#     #                                     related_name='blogs_subscribed',
#     #                                     on_delete=models.CASCADE, null=True)
#     # subscribes = models.ForeignKey(User,
#     #                                related_name='blogs_subscribed', on_delete=models.CASCADE,
#     #                                blank=True, null=True)

#     def __str__(self):
#         return f'{self.user.username}\'s blog!'


# class BlogUser(User):
#     subscribed_blogs = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='user')


class Post(models.Model):
    # define standard and custom managers
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    # The tags manager will allow you to add, retrieve, and remove tags
    # from Post objects
    # tags = TaggableManager()

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)

    # slug (short name) is unique with field 'publish'
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='published')

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts', )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # slug generation for title
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post-detail',
                       kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f'{self.title} by {self.author.username}'


# class NewsPost(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)

#     read = models.BooleanField(default=False)
#     added = models.DateTimeField(auto_now=True)

#     blog = models.ForeignKey(Blog, models.CASCADE, related_name='news_feed')

#     class Meta:
#         ordering = ('-added',)

#     def __str__(self):
#         return f'Owner: {self.blog.user.username}. Slug: {self.post.slug}. From: {self.post.blog.user.username}'

#     def get_absolute_url(self):
#         return reverse('blog:news-post-detail',
#                        kwargs={'pk': self.pk})


# def create_blog_for_new_user(sender, instance, signal, *args, **kwargs):
#         Blog(user=instance).save()


# def news_feeds_update(sender, instance, signal, *args, **kwargs):
#     subscribed_blogs = instance.blog.user.blogs_subscribed.all()
#     send_mails_to_subscribers(instance.blog.user, subscribed_blogs, instance)
#     for blog in subscribed_blogs:
#         news = NewsPost(blog=blog,
#                         post=instance,
#                         )
#         news.save()


def send_mails_to_subscribers(sender, blogs, post):
    recipients = [blog.user.email for blog in blogs]
    full_url = ''.join(['http://', Site.objects.get_current().domain, ':8000', post.get_absolute_url()])
    subject = f'{sender} has published a post'
    message = f'{sender} has posted a new post: {post.title}' \
    f'Read {post.title} at {full_url}'
    args = [subject, message, 'blog_nekidaem@vas.sovsem', recipients]
    result = loop.run_in_executor(None, start_sending, args)
    return result

def start_sending(args):
    result = 0
    try:
        result = send_mail(args[0], args[1], args[2], args[3])
        logging.info(f'mail to {args[3]} has been sent. Result = {result}.')
    except ConnectionRefusedError:
        logging.info(f'Error while sending mail to {args[3]}.')
    return result

# subscribe a handler to post_save CustomerUser event
# signals.post_save.connect(news_feeds_update, sender=Post)
# signals.post_save.connect(create_blog_for_new_user, sender=User)
