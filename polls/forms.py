from django import forms
from .models import Choice, Question

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
