from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import signals
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

# Create your models here.



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset() \
            .filter(status='published')


class Blog(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)

    # users_subscribe = models.ForeignKey(User,
    #                                     related_name='blogs_subscribed',
    #                                     on_delete=models.CASCADE, null=True)
    subscribes = models.ManyToManyField(User,
                                        related_name='blogs_subscribed',
                                        blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}\'s blog!'


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

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,
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
        return f'{self.title} by {self.blog.user.username}'


class NewsPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    read = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now=True)

    blog = models.ForeignKey(Blog, models.CASCADE, related_name='news_feed')

    class Meta:
        ordering = ('-added',)

    def __str__(self):
        return f'Owner: {self.blog.user.username}. Slug: {self.post.slug}. From: {self.post.blog.user.username}'

    def get_absolute_url(self):
        return reverse('blog:news-post-detail',
                       kwargs={'pk': self.pk})


def news_feeds_update(sender, instance, signal, *args, **kwargs):
    subscribed_blogs = instance.blog.user.blogs_subscribed.all()
    for blog in subscribed_blogs:
        news = NewsPost(blog=blog,
                        post=instance,
                        )
        news.save()

    # Send verification email
    # send_verification_email.delay(instance.pk)


# subscribe a handler to post_save CustomerUser event
signals.post_save.connect(news_feeds_update, sender=Post)
