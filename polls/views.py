from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, JsonResponse
from django.urls import reverse, reverse_lazy
from django.db.models.query import QuerySet
from django.contrib import messages
from django.utils import timezone
from django.db.models import F
from urllib.parse import urlencode, quote
from typing import Any
from reversion.models import Version
import reversion

from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views import View

from .models import Choice, Question, Reply
from .forms import QuestionForm, ReplyForm


class QuestionListView(ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    model = Question

    def get_queryset(self):
        query = super().get_queryset().filter(pub_date__lte=timezone.now())
        sort_by = self.request.GET.get('sort_by', 'newest')
        sorting_options = {'newest': '-pub_date', 'oldest': 'pub_date',}
        selected_sort = sorting_options.get(sort_by, '-pub_date')
        return query.order_by(selected_sort)
    
    def get_context_data(self, **kwargs):
        # Add the form to the context data for the GET request
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', QuestionForm())
        context['title'] = 'wisqer'
        context['current_sort_option'] = self.request.GET.get('sort_by', 'newest')
        context['sorting_labels'] = {'newest': 'Newest', 'oldest':'Oldest',}
        return context


class QuestionCreateView(LoginRequiredMixin, FormView):
    form_class = QuestionForm
    template_name = "polls/index.html"
    success_url = reverse_lazy('polls:index')
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'next'

    def form_valid(self, form):
        with reversion.create_revision():
            new_question = form.save(commit=False)
            new_question.user = self.request.user
            new_question.pub_date = timezone.now()
            new_question.save()

            reversion.set_user(self.request.user)
        #encoded_question = quote(new_question.question_text)
        return HttpResponseRedirect(
            reverse('polls:detail', args=(new_question.id, new_question.question_text,))
        )
    
    def form_invalid(self, form):
        latest_question_list = Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
        context = self.get_context_data(form=form)
        context['latest_question_list'] = latest_question_list
        context['errors'] = form.errors
        return render(self.request, 'polls/index.html', context)


class QuestionReplyView(TemplateView):
    template_name = "polls/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_obj = get_object_or_404(
            Question.objects.filter(
                pub_date__lte=timezone.now()
                ), pk=kwargs["question_id"]
        )
        context['question'] = question_obj
        context['question_update_form'] = QuestionForm(instance=question_obj)
        versions = Version.objects.get_for_object(question_obj)
        context['versions'] = versions
        context['reply_form'] = ReplyForm()

        highlighted_reply_id = self.request.GET.get('reply_id')

        latest_reply_list = list(Reply.objects.filter(
        pub_date__lte=timezone.now(),
        question=question_obj
        ).exclude(id=highlighted_reply_id).order_by('-pub_date'))

        if highlighted_reply_id:
            highlighted_reply = get_object_or_404(
                Reply, id=highlighted_reply_id, question=question_obj
                )
            context['highlighted_reply_id'] = highlighted_reply.id
            latest_reply_list.insert(0, highlighted_reply)

        context['latest_reply_list'] = latest_reply_list
        context['title'] = question_obj.question_text
        return context


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'next'

    def post(self, request, pk, question_text):
        question = get_object_or_404(Question, pk=pk)
        if question.user != request.user:
            return HttpResponseForbidden("Unable to delete question")
        question.delete()
        return HttpResponseRedirect(reverse('polls:index'))
    
    def test_func(self):
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return self.request.user == question.user
    

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'next'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        with reversion.create_revision():
            question = form.save(commit=False)
            question.user = self.request.user
            question.pub_date = question.pub_date
            question.save()
            reversion.set_user(self.request.user)

        return JsonResponse({'success':True, 'message': 'Question updated successfully.'})
    
    def form_invalid(self, form):
        return JsonResponse({'success':False, 'errors': form.errors}, status=400)
    
    def test_func(self):
        question = self.get_object()
        return question.user == self.request.user    


class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('accounts:login')

    def post(self, request, pk):
        reply = get_object_or_404(Reply, pk=pk)
        question = reply.question
        if reply.user != request.user:
            return HttpResponseForbidden("Unable to delete reply")
        reply.delete()
        #encoded_question = quote(question.question_text)
        return HttpResponseRedirect(reverse('polls:detail', args=(question.id, question.question_text,)))
    
    def test_func(self):
        reply = get_object_or_404(Reply, pk=self.kwargs['pk'])
        return self.request.user == reply.user


class ReplyCreateView(LoginRequiredMixin, FormView):
    form_class = ReplyForm
    template_name = "polls/detail.html"
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'next'

    def get_success_url(self):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        return reverse_lazy('polls:detail', args=(self.kwargs['question_id'], question.question_text,))

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        new_reply = form.save(commit=False)
        new_reply.user = self.request.user
        new_reply.pub_date = timezone.now()
        new_reply.question = question
        new_reply.save()

        return super().form_valid(form)
    
    def form_invalid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        context = self.get_context_data(form=form)
        context['question'] = question
        versions = Version.objects.get_for_object(question)
        context['versions'] = versions
        context['reply_form'] = form

        latest_reply_list = Reply.objects.filter(
            pub_date__lte=timezone.now(),
            question=question
        ).order_by('-pub_date')

        context['latest_reply_list'] = latest_reply_list
        context['title'] = f"Could not reply to {question.question_text}"
        return self.render_to_response(context)


class ResultsView(DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST["choice"])
        
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form.
        context = {
            "question":question,
            "error_message": "You didn't select a choice.",
        }
        return render(request, "polls/detail.html", context)
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", \
                                            args=(question.id,)))
