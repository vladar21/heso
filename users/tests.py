from django.test import TestCase
from django.urls import reverse
from .forms import UserRegisterForm


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
