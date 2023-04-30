from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser

class SignupViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        self.customer_group = Group.objects.create(name='Customer')

    def test_signup_view_post(self):
        response = self.client.post(self.url, data=self.user_data)
        print(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:home'))
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())
        user = CustomUser.objects.get(username='testuser')
        self.assertTrue(self.customer_group in user.groups.all())

    def test_signup_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertTrue(isinstance(response.context['form'], CustomUserCreationForm))
        self.assertFalse(response.context['form'].is_bound)

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class SigninViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

    def test_signin_view_get(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Sign In')

    def test_signin_view_post_valid(self):
        response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertRedirects(response, reverse('main:home'))

    def test_signin_view_post_invalid(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username='testuser2',
            password='testpass123'
        )

        # Submit an invalid login form with incorrect password
        data = {
            'username': 'testuser2',
            'password': 'incorrectpassword'
        }
        response = self.client.post(reverse('signin'), data)

        # Verify that the user is not authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)





