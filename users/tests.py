# users/tests.py

from django.test import TestCase
from django.urls import reverse
from django.core import mail

from .forms import UserRegisterForm
from .models import User


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
        self.assertEqual(response.status_code, 302)  # Redirect to login page
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


class LogoutTest(TestCase):
    def test_logout_redirect(self):
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)  # Check redirection to login page


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