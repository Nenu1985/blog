from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset() \
            .filter(status='published')


class Blog(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    users_subscribe = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                             related_name='blogs_subscribed',
                                             blank=True)

    def __str__(self):
        return f'{self.user.username}\'s blog!'


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
                              default='draft')

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,
                              related_name='posts',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # slug generation for title
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class NewsPost(models.Model):

    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    read = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now=True)

    blog = models.ForeignKey(Blog, models.CASCADE, related_name='news_feed')

    class Meta:
        ordering = ('-added',)

    def __str__(self):
        return f'News Item of {self.post.slug}'
