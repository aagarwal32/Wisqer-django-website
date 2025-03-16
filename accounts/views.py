from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse, reverse_lazy

from accounts.forms import UserCreationForm
from accounts.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
from django.contrib import messages
from django.utils import timezone
from djangodocker import settings

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import TemplateView
from django.views import View

from polls.models import Question, Reply
from accounts.models import UserFollowing
from . tokens import generate_token
User = get_user_model()


# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # ensure no email duplicates
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return render(request, 'accounts/register.html', {'form': form})
            
            # save user if all checks pass
            user = form.save()
            user.is_active = False
            user.save()
            print(f"User registered. User active? {user.is_active}")

            try:
                # Send the verification link for account activation
                current_site = get_current_site(request)
                subject = "Confirm your email to activate your WISQER account"
                message = render_to_string("accounts/email_confirmation.html", {
                    'username': user.username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user)
                })
                email_confirmation = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                email_confirmation.fail_silently = True
                email_confirmation.send()
                messages.success(request, "Your account has been successfully created. Please check your email to activate your account.")

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def activate(request, uidb64, token):
    print("In activate view")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        return render(request, 'accounts/activation_failed.html')


def login_user(request):
    get_url = request.GET.get('next', reverse('polls:index'))

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(f"User logged in. User active? {user.is_active}")

            # check if user is active (user confirmed email)
            if not user.is_active:
                messages.error(request, "Please confirm your email to log in.")
                return redirect(reverse('accounts:login'))

            login(request, user)
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
    

# FOLLOW VIEWS
def toggle_follow(request, target_user):
    current_user = request.user
    # prevent following yourself
    if current_user == target_user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    follow = UserFollowing.objects.filter(user_id=current_user, following_user_id=target_user)
    if follow.exists():
        follow.delete()
        return JsonResponse({"status": f"remove_user_follow", "message": f"removed follow from user"})
    else:
        UserFollowing.objects.create(user_id=current_user, following_user_id=target_user)
        return JsonResponse({"status": f"add_user_follow", "message": f"added follow to user"})


# Follow view for question users
class QuestionUserFollowView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Question, pk=pk)
        target_user = post.user
        return toggle_follow(request, target_user)

# Follow view for reply users
class ReplyUserFollowView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Reply, pk=pk)
        target_user = post.user
        return toggle_follow(request, target_user)

# Follow view for account users
class AccountUserFollowView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        target_user = get_object_or_404(User, pk=pk)
        return toggle_follow(request, target_user)
