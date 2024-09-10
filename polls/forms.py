from django import forms
from .models import Choice, Question, Reply

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        labels = {
            'question_text': "",
        }
        widgets = {
            'question_text': forms.Textarea(attrs={
                'placeholder':'Enter your question here',
                'rows': '5',
                'cols': '40',
                })
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_text']
        labels = {
            'reply_text': "",
        }

        widgets = {
            'reply_text': forms.Textarea(attrs={
                'placeholder':'Enter your reply here',
                'rows': '3',
                'cols': '80',
                })
        }
