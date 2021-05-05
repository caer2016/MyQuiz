from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from .models import Courses
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

def show_courses_list(request):
    data={'courses': Courses.objects.filter(~Q(student=request.user)).order_by("beginDate")}
    if data:
        return render(request, 'course_pages/courses_list.html', data)
    else:
        return HttpResponse("Hiện tại chưa có khóa học nào")

def course_data(request, id):
    courseInfo = Courses.objects.get(id=id)
    return render(request, 'course_pages/course_info.html', {'course': courseInfo})

def register_course(request, id):
    course = Courses.objects.get(id=id)
    course.student.add(request.user)

    for pack in course.required.all():
        register_pack(request.user, pack.id)

    return redirect('courses')

def unregistered_quizpack_list_view(request):
    unregistered_pack_list = QuizPack.objects.filter(~Q(registered_user=request.user))
    return render(request, 'user_pages/quizpack_list.html', {'pack_list':unregistered_pack_list})

def register_quizpack_view(request, id):
    register_pack(request.user, id)
    return redirect('all_quizpack')

def unregister_quizpack_view(request, id):
    unregister_pack(request.user, id)
    return redirect('student_dashboard')

def teacher_dashboard(request):
    courses_list = Courses.objects.filter(manageTeacher = request.user)
    return render(request, 'user_pages/teacher_dashboard.html', {'courses_list' : courses_list})

def create_new_course(request):
    if not is_teacher(request.user):
        return redirect('index')

    if request.method=='POST':
        newCourseName = request.POST['newCourseName']
        newManageTeacher = request.user
        curC = Courses.objects.create(courseName = newCourseName, manageTeacher = newManageTeacher)
        curC.save()

        return redirect('edit_course', curC.id)

    return render(request, "course_pages/new_course.html")

def edit_course(request, id):
    request.session['current_course_id']=id
    course = get_object_or_404(Courses, id=id)
    added_pack_list = course.required.all()
    all_pack_list = QuizPack.objects.filter(~Q(required=course))

    return render(request, 'course_pages/edit_course.html', {'course': course, 'added_pack_list' : added_pack_list, 'all_pack_list' : all_pack_list})

def add_pack_to_course(request, courseid, packid):
    course = get_object_or_404(Courses, id=courseid)
    pack = get_object_or_404(QuizPack, id=packid)

    if pack not in course.required.all():
        course.required.add(pack)

        for student in course.student.all():
            register_pack(student, pack.id)
    
    return redirect('edit_course', courseid)

def remove_pack_from_course(request, courseid, packid):
    course = get_object_or_404(Courses, id=courseid)
    pack = get_object_or_404(QuizPack, id=packid)

    if pack in course.required.all():
        course.required.remove(pack)
    
    return redirect('edit_course', courseid)