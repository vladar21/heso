# users/views.py

from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .forms import UserRegisterForm


def register(request):
    """
    Register a new user as a student.

    Redirects authenticated users to the schedule page. If the form is valid,
    creates a new user, sends a welcome email, and redirects to the schedule page.
    Otherwise, renders the registration form again.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Rendered webpage or redirection.
    """
    if request.user.is_authenticated:
        return redirect("schedule")
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.save()

            # Creating welcome email
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")

            # Compose and send the email
            subject = "Welcome to HESO!"
            message = f"Hi {username}, thank you for registering at HESO-site."
            from_email = "noreply@heso.com"
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, f"Account created for {username}!")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


def home(request):
    """
    Redirect authenticated users to the schedule page.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Redirection to the schedule page.
    """
    return redirect("/schedule")


def custom_logout(request):
    """
    Log out the current user and redirect to the login page.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse: Redirection to the login page.
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


class LoginView(BaseLoginView):
    """
    Handle user login with customized behavior.

    Extends Django's BaseLoginView to redirect authenticated users,
    display success or error messages based on form validation, and prevent caching.
    """

    template_name = "users/login.html"
    authentication_form = AuthenticationForm  # Ensure correct form is used
    success_url = reverse_lazy(
        "schedule"
    )  # Redirect to 'schedule' after successful login

    def form_valid(self, form):
        """
        Handle successful form validation.

        Adds a success message and redirects to the defined success URL.

        Args:
            form: AuthenticationForm object.

        Returns:
            HttpResponse: Redirection to the success URL.
        """
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle unsuccessful form validation.

        Adds an error message and re-renders the form.

        Args:
            form: AuthenticationForm object.

        Returns:
            HttpResponse: Rendered form with error messages.
        """
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        """
        Redirect authenticated users to the success URL.

        Prevents authenticated users from accessing the login page
        by redirecting them to the success URL.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: Redirection to the success URL or rendered template.
        """
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(*args, **kwargs)
