from django.shortcuts import render,redirect,get_object_or_404
from dashboard.decorators import role_base
from .forms import CourseForm,SectionForm,LessonForm
from .models import Section,Course,Lesson
from enrollments.models import Enrollment
from quizzes.models import QuizResult

# Create your views here.
@role_base('instructor')
def create_course(request):
    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST,request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('instructor_dashboard')
    else:
        form = CourseForm()
    return render(request,'create_course.html',{'course_form':form})

@role_base('instructor')
def edit_course(request,course_id):
    course = Course.objects.get(id = course_id,instructor = request.user)
    form = CourseForm(request.POST,request.FILES,instance=course)
    if form.is_valid():
        form.save()
    return redirect('manage_course',course_id)

@role_base('instructor')
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete() 
    return redirect('instructor_dashboard')


# @role_base('instructor')
# def course_builder(request):
#     return render(request,'course_builder.html')

@role_base('instructor')
def add_section(request,course_id):
    course = get_object_or_404(Course,id=course_id,instructor=request.user)
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.course = course
            if not section.order:
                section.order=course.sections.count()+1
            section.save()
    return redirect('manage_course',course_id)

@role_base('instructor')
def edit_section(request,section_id):
    section = Section.objects.get(id = section_id)
    course_id=section.course.id

    if request.method == 'POST':
        section.title = request.POST.get('title')
        section.order = request.POST.get('order')
        section.save()
    return redirect('manage_course',course_id)



@role_base('instructor')
def delete_section(request, section_id):
    section = Section.objects.get(id=section_id)
    course_id = section.course.id

    section.delete() 
    return redirect('manage_course', course_id)

@role_base('instructor')
def delete_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    course_id = lesson.section.course.id

    lesson.delete()
    return redirect('manage_course', course_id)


@role_base('instructor')
def add_lesson(request,section_id):
    form = LessonForm()
    section = get_object_or_404(Section,id=section_id)
    if request.method == 'POST':
        form = LessonForm(request.POST,request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.section = section

            if not lesson.order:
                lesson.order = section.lessons.count()+1

            lesson.save()
            return redirect('manage_course',section.course.id)
        else:
            print(form.errors)
    return render(request,'add_lesson.html',{'lessonform':form})

@role_base('instructor')
def edit_lesson(request,lesson_id):
    lesson = Lesson.objects.get(id = lesson_id)
    section = lesson.section

    if request.method == 'POST':
        form = LessonForm(request.POST,request.FILES,instance=lesson)
        if form.is_valid:
            form.save()
            return redirect('manage_course',section.course.id)
    else:
        form = LessonForm(instance=lesson)
    
    return render(request,'edit_lesson.html',{'lessonform':form,'lesson':lesson})

@role_base('instructor')
def manage_course(request,course_id):
    course = Course.objects.get(id=course_id, instructor=request.user)
    sections = Section.objects.filter(course=course).prefetch_related('lessons')
    preview_lesson = (Lesson.objects.filter(section__course=course, is_preview=True)
                      .order_by('order').first()
                    )
    course_form = CourseForm(instance=course)
    return render(request,'manage_course.html',{
        'course':course,
        'sections':sections,
        'course_form':course_form,
        'section_form':SectionForm(),
        'lesson_form':LessonForm(),
        'preview_lesson':preview_lesson
    })

@role_base('student')
def course_list(request):
    courses = Course.objects.all()
    enrolled_course_ids = []
    if request.user.is_authenticated:
        enrolled_course_ids = Enrollment.objects.filter(
            student=request.user
        ).values_list('course_id', flat=True)
    return render(request,'course_list.html',{'courses':courses,'enrolled_course_ids':enrolled_course_ids})

@role_base('student')
def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)

    sections = (Section.objects.filter(course=course)
                .select_related('quiz')
                .prefetch_related('lessons')
                )

    preview_lesson = (Lesson.objects.filter(section__course=course, is_preview=True)
                      .order_by('order')
                      .first()
                      )
    

    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).exists()

    
    results = QuizResult.objects.filter(
        student=request.user,
        quiz__section__course=course
    )

    
    for section in sections:
        section.quiz_result = None
        if section.quiz:
            section.quiz_result = results.filter(
                quiz=section.quiz
            ).first()

    return render(request,'course_detail.html',
                  {'course': course,
                   'sections': sections,
                   'is_enrolled': is_enrolled,
                   'preview_lesson':preview_lesson})