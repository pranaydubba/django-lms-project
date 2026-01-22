from django.shortcuts import redirect, get_object_or_404
from dashboard.decorators import role_base
from courses.models import Course
from .models import Enrollment

@role_base('student')
def enrole_course(request, course_id):
    enrollments=Enrollment.objects.filter(student=request.user)
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    return redirect('student_dashboard')
