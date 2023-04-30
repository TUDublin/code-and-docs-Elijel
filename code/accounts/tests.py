"""
Tests for accounts app.
"""

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser


class SignupViewTestCase(TestCase):
    """
    Test case for the SignupView.
    """
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
        """
        Test the SignupView with POST request.
        """
        self.client.post(self.url, data=self.user_data)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())
        user = CustomUser.objects.get(username='testuser')
        self.assertTrue(self.customer_group in user.groups.all())

    def test_signup_view_get(self):
        """
        Test the SignupView with GET request.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertTrue(isinstance(response.context['form'], CustomUserCreationForm))
        self.assertFalse(response.context['form'].is_bound)


class SigninViewTestCase(TestCase):
    """
    Test case for the SigninView.
    """
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

    def test_signin_view_get(self):
        """
        Test the SigninView with GET request.
        """
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Sign In')

    def test_signin_view_post_valid(self):
        """
        Test the SigninView with valid POST request.
        """
        response = self.client.post(reverse('signin'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertRedirects(response, reverse('main:home'))

    def test_signin_view_post_invalid(self):
        """
        Test the SigninView with invalid POST request.
        """
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
