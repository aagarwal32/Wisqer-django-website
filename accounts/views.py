from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy

from accounts.forms import UserCreationForm
from accounts.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import TemplateView
from django.views import View

from polls.models import Question, Reply
User = get_user_model()


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


class AccountPageView(TemplateView):
    template_name = "accounts/account_page.html"

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])

        context = super().get_context_data(**kwargs)
        user_questions = Question.objects.filter(
                pub_date__lte=timezone.now(),
                user=user.id
        ).order_by('-pub_date')
        
        user_replies = Reply.objects.filter(
            pub_date__lte=timezone.now(),
            user=user.id
        ).order_by('-pub_date')
        
        context['account_user'] = user
        context['user_question_list'] = user_questions
        context['user_reply_list'] = user_replies
        context['title'] = f"{user.username}'s Account Page"
        return context


class AccountDeleteView(LoginRequiredMixin, View):
    success_url = reverse_lazy('accounts:login')
    
    def post(self, request):
        deleted_user = User.objects.get(username='[deleted]')
        
        # anonymize user
        user = request.user
        user.question_set.update(user=deleted_user)
        user.reply_set.update(user=deleted_user)

        # delete user
        user.delete()

        # logout user
        logout(request)
        messages.success(request, "Your account has been successfully anonymized and deleted.")

        return HttpResponseRedirect(self.success_url)
    
