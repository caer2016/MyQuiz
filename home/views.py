from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from user import forms
from .models import ClassModel

# Create your views here.
def index(request):
    return render(request, 'pages/home.html')

def login(request):
    return render(request, 'pages/login.html')

def register(request):
    userForm = forms.QUserForm()
    my_dict = {'userForm':userForm, }
    print(my_dict)
    if request.method=='POST':
        userForm = forms.QUserForm(request.POST)
        if userForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            if request.POST.get('user_select', False) == 'student':
                my_student_group = Group.objects.get_or_create(name='STUDENT')
                my_student_group[0].user_set.add(user)
            if request.POST.get('user_select', False) == 'teacher':
                my_student_group = Group.objects.get_or_create(name='TEACHER')
                my_student_group[0].user_set.add(user)
        return HttpResponseRedirect("/login/")
    return render(request,'pages/register.html',context = my_dict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def after_login(request):
    if is_student(request.user):
        return redirect('/user/student_dashboard/')
    elif is_teacher(request.user):
        return redirect('/user/teacher_dashboard/')

def show_class_list(request):
    #data = {'Classes': ClassModel.objects.all().order_by("-beginDate")}
    return render(request, 'pages/classes.html', data)

def find_info(request): 
    return render(request, 'pages/search_info.html')