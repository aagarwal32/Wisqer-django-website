from django.urls import path
from . import views
from .views import *

app_name = "polls"
urlpatterns = [
    # /polls/
    path("", QuestionListView.as_view(), name="index"),
    path("<str:username>/bookmarks/", BookmarkListView.as_view(), name="bookmarks"),
    path("<str:username>/<int:pk>/following/", FollowListView.as_view(), name="following"),
    path("about/", AboutView.as_view(), name="about"),
    path("post/", QuestionCreateView.as_view(), name="create_question"),
    path("post/<int:question_id>/<str:question_text>/", QuestionReplyView.as_view(), name="detail"),
    path("post/<int:pk>/<str:question_text>/rate", QuestionRatingView.as_view(), name="question_rating"),
    path("post/<int:pk>/<str:question_text>/bookmark", QuestionBookmarkView.as_view(), name="question_bookmark"),
    path("post/<int:pk>/<str:question_text>/delete/", QuestionDeleteView.as_view(), name="question_delete"),
    path("post/<int:pk>/<str:question_text>/update/", QuestionUpdateView.as_view(), name="question_update"),
    path("reply/<int:question_id>/<str:question_text>/", ReplyCreateView.as_view(), name="create_reply"),
    path("wisqerai/<int:pk>/<str:question_text>/", WisqerBotView.as_view(), name="wisqer_bot"),
    path("reply/<int:pk>/<str:reply_text>/rate", ReplyRatingView.as_view(), name="reply_rating"),
    path("reply/<int:pk>/<str:reply_text>/bookmark", ReplyBookmarkView.as_view(), name="reply_bookmark"),
    path("reply/<int:pk>/<str:reply_text>/delete/", ReplyDeleteView.as_view(), name="reply_delete"),
    path("search/", views.search_view, name='search'),
]