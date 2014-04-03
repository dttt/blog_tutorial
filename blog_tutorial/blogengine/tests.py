from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from blogengine.models import Post


class PostTest(TestCase):

    def test_create_post(self):
        # Creates first post to test
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
        post.slug = 'my-first-post'
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


class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()


class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']

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
            'pub_date_1': '22:00:03',
            'slug': 'my-second-post'
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
        post.slug = 'my-first-post'
        post.save()

        # Log in
        self.client.login(username='admintest', password="totalwar")

        # Edit the post
        response = self.client.post(
            '/admin/blogengine/post/' +
            str(post.id) +
            '/', {
                'title': 'My second post',
                'text': 'This is my second blog post',
                'pub_date_0': '2013-12-28',
                'pub_date_1': '22:00:04',
                'slug': 'my-second-post'
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
        post.slug = 'my-first-post'
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        # Log in
        self.client.login(username='admintest', password="totalwar")

        # Delete the post
        response = self.client.post(
            '/admin/blogengine/post/' +
            str(post.id) +
            '/delete/', {
                'post': 'yes'
            }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check post amended
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 0)


class PostViewTest(BaseAcceptanceTest):

    def setUp(self):
        # Setup the first post
        self.post = Post()
        self.post.title = 'My first post'
        self.post.text = 'This is my first blog post'
        self.post.pub_date = timezone.now()
        self.post.slug = 'my-first-post'
        self.post.save()
        # Get the first post
        self.only_post = Post.objects.all()[0]

    def test_index(self):
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

        response = self.client.get(reverse('blogs:index'))
        self.assertEquals(response.status_code, 200)

        self.assertTrue(self.post.title in response.content)

        self.assertTrue(self.post.text in response.content)

        self.assertTrue(str(self.post.pub_date.year) in response.content)
        self.assertTrue(self.post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(self.post.pub_date.day) in response.content)

    def test_post_page(self):
        #post_url = self.only_post.get_absolute_url()

        response = self.client.get(reverse(
            'blogs:detail',
            args=[self.only_post.id])
        )
        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.post.title in response.content)

        #self.assertTrue(srt(post.pub_date))
