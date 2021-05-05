from django.shortcuts import render
from django.http import HttpResponse
from . import forms
from .models import QUser, Courses
from home.views import is_teacher, is_student

# Create your views here.

def student_dashboard(request):
    return render(request, 'user_pages/student_dashboard.html')

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
