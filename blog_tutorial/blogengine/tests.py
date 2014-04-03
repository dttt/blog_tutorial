from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone

from blogengine.models import Post


class PostTest(TestCase):

    def test_create_post(self):
        # Creates first post to test
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.save()

        # Tests if first post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        # Checks first post saved success
        self.assertEqual(only_post, post)
        # Check first post content saved success
        # self.assertEquals(only_post.title, 'My first post')
        self.assertEquals(only_post.text, 'This is my first blog post')
        self.assertEquals(only_post.pub_date.day, post.pub_date.day)
        self.assertEquals(only_post.pub_date.month, post.pub_date.month)
        self.assertEquals(only_post.pub_date.year, post.pub_date.year)
        self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
        self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
        self.assertEquals(only_post.pub_date.second, post.pub_date.second)


class AdminTest(LiveServerTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()

    def test_login(self):
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Log in' in response.content)
        # Logs the user in
        self.client.login(username='dttt', password='totalwar')
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Log out' in response.content)

    def test_logout(self):
        self.client.login(username='dttt', password='totalwar')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Log out' in response.content)
        self.client.logout()
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Log in' in response.content)
