from django.shortcuts import render
from .models import *
from django.utils.timezone import now
from datetime import timedelta

def start_learn_pack(request, id):

    quiz_pack = QuizPack.objects.get(id = id)
    schedules = QuestionSchedule.objects.filter(user = request.user, question__pack = quiz_pack, scheduled_time__lte = now())
    request.session['schedules_query'] = schedules

    return learning_view(request)

def start_learn_all(request):

    schedules = QuestionSchedule.objects.filter(user = request.user,  scheduled_time__lte = now())
    request.session['schedules_query'] = schedules

    return learning_view(request)

def update_schedule(request, schedule, correct : bool):

    if correct:
        schedule.previous_interval *= 2 
        schedule.scheduled_time = now() + schedule.previous_interval
    else:
        schedule.previous_interval = timedelta(minutes = 10) 
        schedule.scheduled_time = now() + timedelta(minutes = 10) 

def learning_view(request, schedule_query = None):

    if request.method == 'POST':
        correct = bool(request.POST['correct'])
        update_schedule(request, request.session.get('learning'), correct)

    learning = request.session.get('scheduled_time').first()
    request.session['learning'] = learning

    return render(request, 'learn.html', {'question' : learning.question})