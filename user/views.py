from django.shortcuts import render
from django.http import HttpResponse
from . import forms
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

def unregistered_quizpack_list_view(request):
    unregistered_pack_list = QuizPack.objects.filter(~Q(registered_user=request.user))
    return render(request, 'user_pages/quizpack_list.html', {'pack_list':unregistered_pack_list})

def register_quizpack_view(request, id):
    register_pack(request.user, id)
    return redirect('all_quizpack')

def unregister_quizpack_view(request, id):
    unregister_pack(request.user, id)
    return redirect('student_dashboard')