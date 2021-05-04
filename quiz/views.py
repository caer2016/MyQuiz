from django.shortcuts import render
from .models import *
from django.utils.timezone import now
from datetime import timedelta
from django.http import HttpResponse 
from django.shortcuts import redirect

def update_schedule(request, schedule, correct : bool):

    if correct:
        schedule.previous_interval *= 2 
        schedule.scheduled_time = now() + schedule.previous_interval
    else:
        schedule.previous_interval = timedelta(minutes = 10) 
        schedule.scheduled_time = now() + timedelta(minutes = 10) 
    
    schedule.save()
    
    print(schedule.scheduled_time)

def learning_view(request, id = None):

    if id==None:
        scheduled = QuestionSchedule.objects.filter(user = request.user, scheduled_time__lte = now())
    else:
        scheduled = QuestionSchedule.objects.filter(user = request.user, question__pack = quiz_pack, scheduled_time__lte = now())

    if request.method == 'POST':
        correct = bool(request.POST['correct'])
        learningid = request.session.get('learning')
        learning = QuestionSchedule.objects.get(id = learningid)

        update_schedule(request, learning, correct)

    if len(scheduled)==0:
        return redirect('learning_complete')

    learning = scheduled.order_by('scheduled_time').first()
    request.session['learning'] = learning.id

    return render(request, 'learn.html', {'question' : learning.question})

def learning_complete(request):

    del request.session['learning']
    return HttpResponse("Complete")
