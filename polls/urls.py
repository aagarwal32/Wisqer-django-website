from django.urls import path
from . import views
from .views import (
    QuestionListView, 
    QuestionCreateView,
    QuestionReplyView,
    QuestionDeleteView,
    ReplyCreateView,
    ReplyDeleteView
    )

app_name = "polls"
urlpatterns = [
    # /polls/
    path("", QuestionListView.as_view(), name="index"),
    path("post/", QuestionCreateView.as_view(), name="create_question"),
    path("post/<int:question_id>/", QuestionReplyView.as_view(), name="detail"),
    path("post/<int:pk>/delete/", QuestionDeleteView.as_view(), name="question_delete"),
    path("reply/<int:pk>/delete/", ReplyDeleteView.as_view(), name="reply_delete"),
    path("reply/<int:question_id>/", ReplyCreateView.as_view(), name="create_reply"),
    path("post/<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("post/<int:question_id>/vote/", views.vote, name="vote"),
]