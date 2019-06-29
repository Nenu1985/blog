from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from blog.models import Blog, Post, NewsPost
from blog.views import SubscribeBlogView, UnsubscribeBlogView
from django.contrib import messages

# >>> from django.test.utils import setup_test_environment
# >>> setup_test_environment()
def setup_view(view, request, *args, **kwargs):
    """
    Mimic ``as_view()``, but returns view instance.
    Use this function to get view instances on which you can run unit tests,
    by testing specific methods.
    """

    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

# Create your tests here.
class DemoTest(TestCase):
    def test_blog_save(self):
        self.john = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        b = Blog(user=self.john)
        b.save()
        self.assertTrue(b, 'Blog creation error')

    def test_user(self):
        self.john = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user = authenticate(username='john', password='johnpassword')

        self.assertTrue(self.user.is_active, 'User login error')
        self.assertTrue(self.user.is_authenticated, 'User login error')


class BlogTest(TestCase):
    def setUp(self):
        self.john = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.andrey = User.objects.create_user('andrey', 'lennon@thebeatles.com', 'johnpassword')
        self.vanya = User.objects.create_user('vanya', 'lennon@thebeatles.com', 'johnpassword')

        self.user = authenticate(username='john', password='johnpassword')

        users = [self.john, self.andrey, self.vanya]
        for user in users:
            b = Blog(user=user)
            b.save()



    def test_blog(self):
        b = Blog.objects.get(user=self.john)
        self.assertTrue(b, 'Blog creation error')

    def test_post_create(self):
        blog_owner = self.john.blog
        post = Post(title='New post', body='Post body', status='published', blog=blog_owner)
        post.save()
        self.assertTrue(post, 'Post creation error')

    def test_manual_subscribe(self):
        subscribes_before = self.john.blog.subscribes.all()
        self.assertEqual(subscribes_before.count(), 0, 'Subscribes count is wrong!')
        self.john.blog.subscribes.add(self.andrey)
        subscribes_after = self.john.blog.subscribes.all()
        self.assertEqual(subscribes_after.count(), 1, 'Subscribes count is wrong!')

        # Check if andrey is still without subscribers:
        self.assertEqual(self.andrey.blog.subscribes.all().count(), 0, 'Subscribes count is wrong!')

    def test_manual_unsubscribe(self):
        # 0 subscribers
        self.john.blog.subscribes.add(self.andrey)
        # 1 subscriber
        subscribes_before = self.john.blog.subscribes.all()
        self.assertEqual(subscribes_before.count(), 1, 'Subscribes count is wrong!')
        self.assertEqual(self.andrey.blog.subscribes.all().count(), 0, 'Subscribes count is wrong!')

        self.john.blog.subscribes.remove(self.andrey)
        # 0 subscriber
        subscribes_after = self.john.blog.subscribes.all()
        self.assertEqual(subscribes_after.count(), 0, 'Subscribes count is wrong!')

        # Check if andrey is still without subscribers:
        self.assertEqual(self.andrey.blog.subscribes.all().count(), 0, 'Subscribes count is wrong!')

    def test_subscribe_by_view(self):
        factory = RequestFactory()

        # Blog owner (john) wanted to subscribe on andrey's blog
        blog_id = self.andrey.blog.id

        request = factory.get("subscribe/", {'blog_id': blog_id,})
        request.user = self.john
        view = setup_view(SubscribeBlogView(), request)

        subscribes_before = self.john.blog.subscribes.all()
        self.assertEqual(subscribes_before.count(), 0, 'Subscribes count is wrong!')

        # Make subscribe
        response = view.get(request, blog_id)

        # Check if subscribe is appeared
        subscribes_after = self.john.blog.subscribes.all()

        self.assertEqual(subscribes_after.count(), 1, 'Subscribes count is wrong!')
        self.assertEqual(subscribes_after.first().username, 'andrey', 'Subscribe incorrect')

        self.assertEqual(response.status_code, 302, 'Status code is wrong')
        self.assertEqual(response.url, '/blog/', 'Redirected url is wrong')

    def test_unsubscribe_by_view(self):
        # Manual subscribe on andrey
        self.john.blog.subscribes.add(self.andrey)

        factory = RequestFactory()

        # Blog owner (john) wanted to unsubscribe from andrey's blog
        blog_id = self.andrey.blog.id

        request = factory.get("unsubscribe/", {'blog_id': blog_id, })
        request.user = self.john
        view = setup_view(UnsubscribeBlogView(), request)

        subscribes_before = self.john.blog.subscribes.all()
        self.assertEqual(subscribes_before.count(), 1, 'Subscribes count is wrong!')
        self.assertEqual(subscribes_before.first().username, 'andrey', 'Subscribe incorrect')

        # Make unsubscribe
        response = view.get(request, blog_id)

        # Check if subscribe is disappeared
        subscribes_after = self.john.blog.subscribes.all()

        self.assertEqual(subscribes_after.count(), 0, 'Subscribes count is wrong!')


        self.assertEqual(response.status_code, 302, 'Status code is wrong')
        self.assertEqual(response.url, '/blog/', 'Redirected url is wrong')

    def test_news_feed(self):
        # John subscribed on andrey:
        self.john.blog.subscribes.add(self.andrey)

        news_in_feeds = [self.john.blog.news_feed.all().count(),
                         self.andrey.blog.news_feed.all().count(),
                         self.vanya.blog.news_feed.all().count(),
                        ]
        self.assertEqual(news_in_feeds, [0, 0, 0], 'News count before post is wrong')

        # andrey posts a post:
        post = Post(title='New post', body='Post body', status='published', blog=self.andrey.blog)
        post.save()
        # John's news-feed must be updated
        news_in_feeds = [self.john.blog.news_feed.all().count(),
                         self.andrey.blog.news_feed.all().count(),
                         self.vanya.blog.news_feed.all().count(),
                         ]
        self.assertEqual(news_in_feeds, [1, 0, 0], 'News count after post is wrong')

        # 1 subscriber