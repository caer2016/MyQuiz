from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('user/student_dashboard/', views.student_dashboard),
    path('user/teacher_dashboard/', views.teacher_dashboard),
    path('user/teacher_dashboard/courses/new_course', views.create_new_course),
    path('courses_list/', views.show_courses_list, name='courses'),
    path('courses_list/<int:id>/', views.course_data, name='course_data'),
]
