from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Section,Course
from .models import Quiz, Question,Option,QuizResult
from .forms import QuestionForm,OptionForm
from dashboard.decorators import role_base

@role_base('instructor')
def add_quiz(request, section_id):
    section = get_object_or_404(Section, id=section_id)

    if request.method == "POST":
        title = request.POST.get("title")
        Quiz.objects.create(section=section, title=title)
    return redirect("manage_course", section.course.id)

@role_base('instructor')
def manage_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == "POST":

        if "add_question" in request.POST:
            qform = QuestionForm(request.POST)
            if qform.is_valid():
                question = qform.save(commit=False)
                question.quiz = quiz
                question.save()
                return redirect("manage_quiz", quiz.id)

        elif "update_question" in request.POST:
            question = get_object_or_404(Question, id=request.POST.get("question_id"))
            qform = QuestionForm(request.POST, instance=question)
            if qform.is_valid():
                qform.save()
                return redirect("manage_quiz", quiz.id)

        elif "delete_question" in request.POST:
            ques=Question.objects.filter(id=request.POST.get("question_id"))
            ques.delete()
            return redirect("manage_quiz", quiz.id)

        elif "add_option" in request.POST:
            question = get_object_or_404(Question, id=request.POST.get("question_id"))
            oform = OptionForm(request.POST)
            if oform.is_valid():
                option = oform.save(commit=False)
                option.question = question
                option.save()
                return redirect("manage_quiz", quiz.id)

        elif "update_option" in request.POST:
            option = get_object_or_404(Option, id=request.POST.get("option_id"))
            oform = OptionForm(request.POST, instance=option)
            if oform.is_valid():
                oform.save()
                return redirect("manage_quiz", quiz.id)

        elif "delete_option" in request.POST:
            option=Option.objects.filter(id=request.POST.get("option_id"))
            option.delete()
            return redirect("manage_quiz", quiz.id)

    return render(request,"manage_quiz.html", {
        "quiz": quiz,
        "questions": questions,
        "qform": QuestionForm(),
        "oform": OptionForm()
    })

@role_base('student')
def start_test(request,quiz_id):
    quiz = get_object_or_404(Quiz,id=quiz_id)

    if QuizResult.objects.filter(student=request.user, quiz=quiz).exists():
        return redirect('test_result',course_id=quiz.section.course.id,quiz_id=quiz.id)

    questions = Question.objects.filter(quiz=quiz).prefetch_related('option_set')

    if request.method == 'POST':
        total_marks=0
        obtained_marks=0

        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            total_marks += question.marks

            if selected_option_id:
                option = Option.objects.get(id=selected_option_id)
                if option.is_correct:
                    obtained_marks += question.marks
            
            

        percentage = round((obtained_marks / total_marks) * 100, 2) if total_marks>0 else 0

        QuizResult.objects.create(
            student=request.user,
            quiz=quiz,
            score=obtained_marks,
            total_marks=total_marks ,
            percentage=percentage
        )

        return redirect('test_result',course_id=quiz.section.course.id,quiz_id=quiz.id)

    return render(request, 'start_test.html', {'quiz': quiz,'questions': questions})

@role_base('student')
def test_result(request,quiz_id, course_id):
    result = get_object_or_404(
        QuizResult,
        student=request.user,
        quiz_id=quiz_id,
        quiz__section__course_id=course_id
    )

    return render(request, 'test_result.html', {
        'result': result,
        'course_id': course_id
    })


