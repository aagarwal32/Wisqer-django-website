from django.urls import path
from . import views
from .views import (
    QuestionListView, 
    QuestionCreateView,
    QuestionReplyView,
    ReplyCreateView,)

app_name = "polls"
urlpatterns = [
    # /polls/
    path("", QuestionListView.as_view(), name="index"),
    path("post/", QuestionCreateView.as_view(), name="create_question"),
    path("post/<int:question_id>/", QuestionReplyView.as_view(), name="detail"),
    path("post/<int:question_id>/reply/", ReplyCreateView.as_view(), name="create_reply"),
    path("post/<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("post/<int:question_id>/vote/", views.vote, name="vote"),
]