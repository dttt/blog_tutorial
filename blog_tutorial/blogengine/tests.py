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

    def test_create_post(self):
        # Tests if posts appear in admin page
        self.client.login(username='dttt', password='totalwar')
        response = self.client.get('/admin/blogengine/post/add/')
        self.assertEquals(response.status_code, 200)
        # Tests create new post through admin page
        response = self.client.post('/admin/blogengine/post/add/', {
            'title': 'My first post',
            'text': 'This is my first post',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:03'
            },
            follow=True
        )
        # Checks added successfully
        self.assertTrue('added successfully' in response.content)
        # Checks new post in database
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

    def test_edit_post(self):
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.save()

        # Log in
        self.client.login(username='admintest', password="totalwar")

        # Edit the post
        response = self.client.post('/admin/blogengine/post/1/', {
            'title': 'My second post',
            'text': 'This is my second blog post',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04'
        },
            follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)

        # Check post amended
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post.title, 'My second post')
        self.assertEquals(only_post.text, 'This is my second blog post')

    def test_delete_post(self):
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        # Log in
        self.client.login(username='admintest', password="totalwar")

        # Delete the post
        response = self.client.post('/admin/blogengine/post/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check post amended
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 0)
