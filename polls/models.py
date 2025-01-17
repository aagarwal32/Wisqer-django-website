from django.db import models
from django.conf import settings
import reversion
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
def get_deleted_user():
    user, created = User.objects.get_or_create(username='[deleted]')
    return user.id


@reversion.register()
class Question(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=get_deleted_user,
    )
    question_text = models.CharField(max_length=200)
    question_body = models.CharField(max_length=2000, blank=True)
    pub_date = models.DateTimeField("date published")
    rating = models.ManyToManyField(User, blank=True, related_name="question_rating")
    bookmark = models.ManyToManyField(User, blank=True, related_name="question_bookmark")

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


@reversion.register()
class Reply(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=get_deleted_user,
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reply_text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField("date published")
    rating = models.ManyToManyField(User, blank=True, related_name="reply_rating")
    bookmark = models.ManyToManyField(User, blank=True, related_name="reply_bookmark")

    def __str__(self) -> str:
        return self.reply_text
    