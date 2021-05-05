from django.shortcuts import render
from django.http import HttpResponse
from . import forms

# Create your views here.

def student_dashboard(request):
    return render(request, 'user_pages/student_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'user_pages/teacher_dashboard.html')