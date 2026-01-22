from django.urls import path
from courses import views

urlpatterns = [
    path('create_course/',views.create_course,name='create_course'),
    path('edit_course/<int:course_id>/',views.edit_course,name='edit_course'),
    path('delete_course/<int:course_id>/',views.delete_course,name='delete_course'),
    path('add_section/<int:course_id>/',views.add_section,name='add_section'),
    path('delete_section/<int:section_id>/',views.delete_section,name='delete_section'),
    path('edit_section/<int:section_id>/',views.edit_section,name='edit_section'),
    path('add_lesson/<int:section_id>/',views.add_lesson,name='add_lesson'),
    path('edit_lesson/<int:lesson_id>/',views.edit_lesson,name='edit_lesson'),
    path('delete_lesson/<int:lesson_id>/',views.delete_lesson,name='delete_lesson'),
    path('manage_course/<int:course_id>/',views.manage_course,name='manage_course'),
    path('course_list/',views.course_list,name='course_list'),
    path('course_detail/<int:course_id>',views.course_detail,name='course_detail'),
]