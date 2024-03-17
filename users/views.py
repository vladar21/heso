from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import logout
from django.core.mail import send_mail


def register(request):
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
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def home(request):
    return redirect('/schedule')


def custom_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')


class LoginView(BaseLoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'You have successfully logged in.')
        return super().form_valid(form)
