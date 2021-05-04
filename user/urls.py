from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('student_dashboard/', views.student_dashboard),
    path('teacher_dashboard/', views.teacher_dashboard),
]
