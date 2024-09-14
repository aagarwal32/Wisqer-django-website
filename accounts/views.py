from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from accounts.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
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
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(f"Logging in user: {user.username}, {user.email}")
            return HttpResponseRedirect(reverse('polls:index'))

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form':form})


def logout_user(request):
    pass