from django.urls import path
from . import views

urlpatterns = [
    path('student_dashboard/', views.student_dashboard),
    path('teacher_dashboard/', views.teacher_dashboard),
]
