from django import forms
from .models import Choice, Question, Reply

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_body']
        labels = {
            'question_text': "",
            'question_body': "",
        }
        widgets = {
            'question_text': forms.Textarea(attrs={
                'placeholder':'Question Title',
                'class':'form-control autoExpand countChars',
                'rows':'1'
                }),
            'question_body': forms.Textarea(attrs={
                'placeholder':'Body (Optional)',
                'class':'form-control autoExpand countChars',
                'rows':'1'
                })
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_text']
        labels = {'reply_text': "",}

        widgets = {
            'reply_text': forms.Textarea(attrs={
                'placeholder':'Enter your reply here',
                'class':'form-control autoExpand countChars',
                'rows':'1',
                }),
        }
