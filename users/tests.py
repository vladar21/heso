# users/tests.py

from django.test import TestCase
from django.urls import reverse
from django.core import mail

from .forms import UserRegisterForm
from .models import User
from django.contrib.auth import get_user_model


class UserRegisterFormTest(TestCase):
    def test_form_valid(self):
        """Test that the user registration form is valid with correct data"""
        form_data = {'username': 'testuser', 'email': 'user@example.com', 'password1': 'dfgjndfgj34', 'password2': 'dfgjndfgj34'}
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        """Test that the user registration form is invalid with incorrect data"""
        form_data = {'username': 'testuser', 'email': 'user', 'password1': 'password', 'password2': 'password'}
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserRegistrationTest(TestCase):
    def test_registration_page_status_code(self):
        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, 200)

    def test_registration_form(self):
        response = self.client.post(reverse('register'), data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 302)  # Redirect to schedule page
        self.assertEqual(len(mail.outbox), 1)  # Check if an email has been sent
    
    def test_duplicate_registration(self):
        """Test that duplicate username or email registration is handled"""
        # Create a user with a specific username and email
        User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')

        # Attempt to register a new user with the same username and email
        response = self.client.post(reverse('register'), data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })

        # Ensure that the registration form displays errors for duplicate username and email
        self.assertFormError(response, 'form', 'username', ['A user with that username already exists.'], msg_prefix='form')
        self.assertFormError(response, 'form', 'email', ['This email address is already in use.'], msg_prefix='form')

        # Ensure that no new user object is created
        self.assertEqual(User.objects.count(), 1)
    
    def test_weak_password_rejected(self):
        """Test that weak passwords are rejected during registration"""
        # Attempt to register a new user with a weak password
        response = self.client.post(reverse('register'), data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password',  # Weak password
            'password2': 'password',
        })

        # Ensure that the registration form displays an error for weak password
        self.assertFormError(response, 'form', 'password2', ['This password is too common.'], msg_prefix='form')

        # Ensure that no new user object is created
        self.assertEqual(User.objects.count(), 0)
    
    def test_edge_cases_handling(self):
        """Test handling of edge cases such as empty form fields or missing required fields"""
        # Attempt to register a new user with empty form fields
        response = self.client.post(reverse('register'), data={
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        })

        # Ensure that the registration form displays errors for missing required fields
        self.assertFormError(response, 'form', 'username', ['This field is required.'], msg_prefix='form')
        self.assertFormError(response, 'form', 'email', ['This field is required.'], msg_prefix='form')
        self.assertFormError(response, 'form', 'password1', ['This field is required.'], msg_prefix='form')
        self.assertFormError(response, 'form', 'password2', ['This field is required.'], msg_prefix='form')

        # Ensure that no new user object is created
        self.assertEqual(User.objects.count(), 0)
    
    def test_logout_verification(self):
        """Test for verifying that the user is actually logged out after the logout request"""
        # Create a user and log them in
        self.client.force_login(User.objects.create_user(username='testuser', password='testpassword123'))

        # Make a request to logout
        response = self.client.get(reverse('logout'), follow=True)

        # Ensure that the user is redirected to the login page after logout
        self.assertEqual(response.status_code, 200)  # Check if the user is redirected successfully
        self.assertTemplateUsed(response, 'users/login.html')  # Ensure that the login page template is used
    
    def test_welcome_email_sent(self):
        """Test to verify that the welcome email is sent after successful user registration"""
        form_data = {'username': 'testuser', 'email': 'testuser@example.com', 'password1': 'dfgjndfgj34', 'password2': 'dfgjndfgj34'}
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(len(mail.outbox), 1)  # Check that one email was sent
    
    def test_email_content_and_recipients(self):
        """Test to check the content and recipients of the sent email"""
        form_data = {'username': 'testuser', 'email': 'testuser@example.com', 'password1': 'dfgjndfgj34', 'password2': 'dfgjndfgj34'}
        response = self.client.post(reverse('register'), data=form_data)
        self.assertEqual(len(mail.outbox), 1)  # Check that one email was sent

        # Check email content
        email = mail.outbox[0]
        self.assertIn('Welcome to HESO!', email.subject)
        self.assertIn('Hi testuser,', email.body)
        self.assertEqual(email.from_email, 'noreply@heso.com')
        self.assertEqual(email.recipients(), ['testuser@example.com'])


class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_login_page_status_code(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_form_valid(self):
        response = self.client.post(reverse('login'), data={
            'username': 'testuser',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Check redirection after login
    
    def test_invalid_username(self):
        """Test that user cannot login with incorrect username"""
        response = self.client.post(reverse('login'), data={
            'username': 'invalid_username',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 200)  # Check that the login page is rendered again
        self.assertContains(response, 'Please enter a correct username')  # Check for error message

    def test_invalid_password(self):
        """Test that user cannot login with incorrect password"""
        response = self.client.post(reverse('login'), data={
            'username': 'testuser',
            'password': 'invalid_password',
        })
        self.assertEqual(response.status_code, 200)  # Check that the login page is rendered again
        self.assertContains(response, 'Invalid username or password. Please try again.')  # Check for error message


class AuthenticatedRedirectTest(TestCase):
    def setUp(self):
        # Create a user and authenticate it
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        self.client.force_login(self.user)

    def test_registration_redirect(self):
        """Test for redirecting authenticated users away from the registration page"""
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('schedule'))

    def test_login_redirect(self):
        """Test for redirecting authenticated users away from the login page"""
        response = self.client.get(reverse('login'), follow=True)
        self.assertRedirects(response, reverse('schedule'), target_status_code=200)

