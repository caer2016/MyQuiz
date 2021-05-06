from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('student_dashboard/', views.student_learn, name = 'student_learn'),
    path('student_learn/', views.student_learn, name = 'student_learn'),
    path('student_add_packs/', views.student_add_packs, name = 'student_add_packs'),
    path('teacher_dashboard/', views.teacher_dashboard, name = 'teacher_dashboard'),
    path('teacher_newCourse/', views.teacher_newCourse, name='teacher_newCourse'),
    path('pack/', views.unregistered_quizpack_list_view, name = 'all_quizpack'),
    path('pack/add/<int:id>', views.register_quizpack_view, name = 'register_pack'),
    path('pack/remove/<int:id>/', views.unregister_quizpack_view, name = 'unregister_pack'),
    path('teacher_dashboard/courses/new_course', views.create_new_course, name='create_course'),
    path('teacher_dashboard/courses/edit/<int:id>/', views.edit_course, name='edit_course'),
    path('teacher_dashboard/courses/addpack/<int:courseid>/<int:packid>/', views.add_pack_to_course, name='add_pack_to_course'),
    path('teacher_dashboard/courses/removepack/<int:courseid>/<int:packid>/', views.remove_pack_from_course, name='remove_pack_from_course'),
    path('teacher_dashboard/pack', views.teacher_pack_list, name='teacher_pack_list'),
    path('courses_list/', views.show_courses_list, name='courses'),
    path('courses_list/<int:id>/', views.course_data, name='course_data'),
    path('courses_list/register/<int:id>/', views.register_course, name='register_course'),
    path('courses_list2/', views.show_courses_list_2, name='courses_list')
]
