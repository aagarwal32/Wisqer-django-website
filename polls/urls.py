from django.urls import path
from . import views
from .views import *

app_name = "polls"
urlpatterns = [
    # /polls/
    path("", QuestionListView.as_view(), name="index"),
    path("post/", QuestionCreateView.as_view(), name="create_question"),
    path("post/<int:question_id>/<str:question_text>/", QuestionReplyView.as_view(), name="detail"),
    path("post/<int:pk>/<str:question_text>/rate", QuestionRatingView.as_view(), name="question_rating"),
    path("post/<int:pk>/<str:question_text>/delete/", QuestionDeleteView.as_view(), name="question_delete"),
    path("post/<int:pk>/<str:question_text>/update/", QuestionUpdateView.as_view(), name="question_update"),
    path("reply/<int:question_id>/<str:question_text>/", ReplyCreateView.as_view(), name="create_reply"),
    path("reply/<int:pk>/delete/", ReplyDeleteView.as_view(), name="reply_delete"),
]