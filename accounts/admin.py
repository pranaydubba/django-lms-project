from django.contrib import admin
from .models import MyUser
from courses.models import Course,Section,Lesson
from enrollments.models import Enrollment
from quizzes.models import Question,Quiz,QuizResult,Option
# Register your models here.

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_approved')
    list_filter = ('role', 'is_approved')
    search_fields = ('email', 'username')
    actions = ['approve_instructors']

    def approve_instructors(self, request, queryset):
        queryset.update(is_approved=True)

    approve_instructors.short_description = "Approve selected instructors"

admin.register(Course)
admin.register(Section)
admin.register(Lesson)
admin.register(Enrollment)
admin.register(Quiz)
admin.register(QuizResult)
admin.register(Option)