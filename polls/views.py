from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question, Reply
from .forms import QuestionForm, ReplyForm


# Create your views here.
def index(request):
    latest_question_list = Question.objects.filter(
        pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:100]
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.pub_date = timezone.now()
            new_question.save()
            return HttpResponseRedirect(reverse('polls:detail', args=(new_question.id,)))

    else:
        form = QuestionForm()

    context = {
        'latest_question_list': latest_question_list,
        'form': form,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    main_question = get_object_or_404(
        Question.objects.filter(pub_date__lte=timezone.now()),
        pk=question_id)
    
    latest_reply_list = Reply.objects.filter(
        pub_date__lte=timezone.now(),
        question=main_question
    ).order_by('-pub_date')[:20]
        
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            new_reply = reply_form.save(commit=False)
            new_reply.question = main_question
            new_reply.pub_date = timezone.now()
            new_reply.save()
            return HttpResponseRedirect(reverse('polls:detail', args=(main_question.id,)))
    else:
        reply_form = ReplyForm()
    context = {
        'question':main_question,
        'reply_form':reply_form,
        'latest_reply_list':latest_reply_list,
    }
    return render(request, "polls/detail.html", context)


class ResultsView(generic.DetailView):
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
