from django.db import models
from django.conf import settings
import reversion
import datetime
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.models import User
from django_resized import ResizedImageField

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
    
    question_img = ResizedImageField(
        null=True,
        blank=True,
        quality=75,
        force_format="WEBP",
        keep_meta=False,
        upload_to="images/"
    )
    
    pub_date = models.DateTimeField("date published")
    rating = models.ManyToManyField(User, blank=True, related_name="question_rating")
    bookmark = models.ManyToManyField(User, blank=True, related_name="question_bookmark")

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text
    

class BookmarkTimestamp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey('Question', null=True, blank=True, on_delete=models.CASCADE)
    reply = models.ForeignKey('Reply', null=True, blank=True, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('user', 'question', 'reply')  # Prevent duplicate bookmarks

    def __str__(self):
        if self.question:
            return f"{self.user.username} bookmarked question {self.question.id} at {self.added_at}"
        if self.reply:
            return f"{self.user.username} bookmarked reply {self.reply.id} at {self.added_at}"
        return f"{self.user.username} bookmark"



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
    