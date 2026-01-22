from django.shortcuts import render,redirect
from .decorators import role_base
from courses.models import Course
from quizzes.models import Quiz,QuizResult
from enrollments.models import Enrollment

# Create your views here.
@role_base('student')
def student_dashboard(request):
    enrollments=Enrollment.objects.filter(student=request.user)
    for enroll in enrollments:
        course = enroll.course

        total_quizzes = Quiz.objects.filter(section__course=course).count()

        completed_quizzes = QuizResult.objects.filter(
            student=request.user,
            quiz__section__course=course
        ).count()

        if total_quizzes > 0:
            enroll.progress = int((completed_quizzes / total_quizzes) * 100)
        else:
            enroll.progress = 0
    return render(request,'student_dashboard.html',{'enrollments':enrollments})

@role_base('instructor')
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor = request.user)
    return render(request,'instructor_dashboard.html',{'courses':courses})

