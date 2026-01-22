from django.urls import path
from enrollments import views

urlpatterns = [
    path('enrole_course/<int:course_id>/',views.enrole_course,name='enrole_course'),
]