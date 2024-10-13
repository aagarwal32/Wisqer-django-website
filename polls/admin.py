from django.contrib import admin
# Register your models here.
from .models import Question, Choice, Reply

admin.site.register(Question)
admin.site.register(Reply)
admin.site.register(Choice)