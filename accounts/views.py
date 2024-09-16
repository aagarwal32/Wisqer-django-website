from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from accounts.forms import UserCreationForm
from accounts.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages


# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.full_clean()
            user = form.save()
            print(f"User created: {user.username}, {user.email}")
            messages.success(request, "Your account has been successfully created. Please login.")
            return HttpResponseRedirect(reverse('accounts:login'))
    
    else: 
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form':form})


def login_user(request):
    get_url = request.GET.get('next', reverse('polls:index'))

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f"Logging in user: {user.username}, {user.email}")
            submit_url = request.POST.get('next', reverse('polls:index'))
            return HttpResponseRedirect(submit_url)

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form':form, 'next':get_url})


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect(reverse('accounts:login'))