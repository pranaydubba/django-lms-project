from django.forms import ModelForm,Form
from django import forms
from .models import Course,Section,Lesson

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title','description','thumbnail','level','language','is_published']
        

class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['title','order']

class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['title','video','notes','is_preview','order']