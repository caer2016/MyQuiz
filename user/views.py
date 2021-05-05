from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from .models import QUser, Courses
from home.views import is_teacher, is_student
from quiz.models import QuizPack, QuestionSchedule
from quiz.views import register_pack, unregister_pack
from django.db.models import Q,Count,F
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now

# Create your views here.

def student_dashboard(request):
    schedule = QuestionSchedule.objects.filter(user=request.user, scheduled_time__lte=now()).values('question__pack').annotate(scheduled_count=Count('question__pack'), name=F('question__pack__name'), id=F('question__pack__id')).order_by('name')
    collection = QuizPack.objects.filter(registered_user = request.user)
    return render(request, 'user_pages/student_dashboard.html', {'schedule' : schedule, 'collection' : collection})

def teacher_dashboard(request):
    return render(request, 'user_pages/teacher_dashboard.html')

def show_courses_list(request):
    data={'courses': Courses.objects.all().order_by("beginDate")}
    if data:
        return render(request, 'course_pages/courses_list.html', data)
    else:
        return HttpResponse("Hiện tại chưa có khóa học nào")

def course_data(request, id):
    courseInfo = Courses.objects.get(id=id)
    return render(request, 'course_pages/course_info.html', {'course': courseInfo})

def create_new_course(request):
    if is_teacher(request.user):
        newCourseName = request.POST['newCourseName']
        newManageTeacher = request.user
        curC = Courses.objects.create(courseName = newCourseName, manageTeacher = newManageTeacher)
        curC.save()

        return render(request, "course_pages/new_course.html")
def unregistered_quizpack_list_view(request):
    unregistered_pack_list = QuizPack.objects.filter(~Q(registered_user=request.user))
    return render(request, 'user_pages/quizpack_list.html', {'pack_list':unregistered_pack_list})

def register_quizpack_view(request, id):
    register_pack(request.user, id)
    return redirect('all_quizpack')

def unregister_quizpack_view(request, id):
    unregister_pack(request.user, id)
    return redirect('student_dashboard')
