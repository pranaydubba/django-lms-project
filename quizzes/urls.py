from django.urls import path
from quizzes import views

urlpatterns = [
    path('add_quiz/<int:section_id>/',views.add_quiz,name='add_quiz'),
    path('manage_quiz/<int:quiz_id>/',views.manage_quiz,name='manage_quiz'),
    path('start_test/<int:quiz_id>/',views.start_test,name='start_test'),
    path('test_result/<int:quiz_id>/<int:course_id>/',views.test_result,name='test_result'),
]