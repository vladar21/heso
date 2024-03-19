# users/views.py

from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .forms import UserRegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect('schedule')  
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.save()

            # Creating welcome email
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Compose and send the email
            subject = 'Welcome to HESO!'
            message = f'Hi {username}, thank you for registering at HESO-site.'
            from_email = 'noreply@heso.com'
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, f'Account created for {username}!')
            return redirect('schedule')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def home(request):
    return redirect('/schedule')


def custom_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    authentication_form = AuthenticationForm  # Ensure correct form is used
    success_url = reverse_lazy('schedule')  # Redirect to 'schedule' after successful login

    def form_valid(self, form):
        messages.success(self.request, 'You have successfully logged in.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)
    
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(*args, **kwargs)

