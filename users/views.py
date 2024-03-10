from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
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
