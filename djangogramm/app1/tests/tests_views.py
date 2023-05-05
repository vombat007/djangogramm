from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from app1.models import User, Post, Image, Like, Hashtag


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('registration')

    def test_register_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_register_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'app1/register.html')

    def test_register_view_form_submission_success(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(self.url, data)
        self.assertTemplateUsed(response, 'app1/email_confirm.html')


class ConfirmEmailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
            is_active=False
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.url = reverse('confirm_email', args=[self.uid, self.token])

    def test_confirm_email_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_confirm_email_view_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'app1/email_confirmed.html')


class App1ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            bio='test user bio',
            avatar='avatars/default.jpg'
        )
        self.post = Post.objects.create(
            user=self.user,
            caption='test post caption'
        )
        self.image = Image.objects.create(
            post=self.post,
            image_file='images/test.jpg'
        )
        self.hashtag = Hashtag.objects.create(
            tag='test'
        )

    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app1/index.html')

    def test_login_page_view(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app1/login.html')

    def test_post_view(self):
        url = reverse('post')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app1/post.html')
        self.assertContains(response, 'test post caption')
