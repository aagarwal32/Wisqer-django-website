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
                'placeholder':'Question title',
                'class':'form-control',
                'rows':'1'
                }),
            'question_body': forms.Textarea(attrs={
                'placeholder':'Question body -- optional',
                'class':'form-control autoExpand',
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
                'class':'form-control autoExpand',
                'rows':'1',
                }),
        }
