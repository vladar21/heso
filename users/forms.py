from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    email = forms.EmailField()
    phone_number = forms.CharField(required=False, help_text="Optional.")

    def clean_username(self):
        """
        Validates that the provided username is unique and not too long.

        Raises:
            ValidationError: If a user with the given username already exists
                or if the length of the username exceeds 150 characters.

        Returns:
            str: The validated username.
        """
        username = self.cleaned_data.get("username")
        if username:
            if User.objects.filter(username=username).exists():
                raise ValidationError("A user with that username already exists.")
        return username

    def clean_email(self):
        """
        Validates that the provided email is unique.

        Raises:
            ValidationError: If a user with the given email already exists.

        Returns:
            str: The validated email.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    class Meta:
        """
        Meta options for UserRegisterForm.

        Attributes:
            model (User): The user model.
            fields (list): List of fields to include in the form.
        """
        model = User
        fields = ["username", "email", "password1", "password2", "phone_number"]
