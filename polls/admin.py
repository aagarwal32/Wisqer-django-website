from django.contrib import admin
# Register your models here.
from .models import Question, Reply

admin.site.register(Question)
admin.site.register(Reply)