from django import forms
from .models import Quiz, Question, Option

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'marks']


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text', 'is_correct']