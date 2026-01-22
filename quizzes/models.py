from django.db import models
from courses.models import Section
from accounts.models import MyUser

class Quiz(models.Model):
    section = models.OneToOneField(Section,on_delete=models.CASCADE,related_name='quiz')
    title = models.CharField(max_length=200)
    total_marks = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.section.title} Quiz"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()
    marks = models.IntegerField(default=1)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


class QuizResult(models.Model):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_marks = models.IntegerField()
    percentage = models.FloatField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'quiz')  

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"