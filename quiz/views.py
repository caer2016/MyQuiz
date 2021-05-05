from django.shortcuts import render
from .models import *
from django.utils.timezone import now
from datetime import timedelta
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, get_object_or_404

DEFAULT_INTERVAL = timedelta(minutes = 10)

def update_schedule(request, schedule, correct : bool):

    if correct:
        schedule.previous_interval *= 2 
        schedule.scheduled_time = now() + schedule.previous_interval
    else:
        schedule.previous_interval = DEFAULT_INTERVAL 
        schedule.scheduled_time = now() + DEFAULT_INTERVAL 
    
    schedule.save()
    
    print(schedule.scheduled_time)

def learning_view(request, id = None):

    if id==None:
        scheduled = QuestionSchedule.objects.filter(user = request.user, scheduled_time__lte = now())
    else:
        quiz_pack = get_object_or_404(QuizPack, id = id)
        scheduled = QuestionSchedule.objects.filter(user = request.user, question__pack = quiz_pack, scheduled_time__lte = now())

    if request.method == 'POST':
        correct = bool(request.POST['correct'])
        learningid = request.session.get('learning')
        learning = QuestionSchedule.objects.get(id = learningid)

        update_schedule(request, learning, correct)

    if len(scheduled)==0:
        return redirect('learning_complete')

    learning = scheduled.order_by('scheduled_time', 'question__id').first()
    request.session['learning'] = learning.id

    return render(request, 'learn.html', {'question' : learning.question, 'packid':id})

def learning_complete(request):

    return render(request, 'learn_complete.html')

def add_pack(request):

    if request.method == 'POST':
        
        try:
            pack_name = request.POST['name']
            category = request.POST['category']
        except:
            return render(request, 'add_pack.html', {'failed' : True})
        
        try:
            description = request.POST['description']
        except:
            description = None

        q = QuizPack.objects.create(name = pack_name, description = description, category = category)
        q.save()
        return redirect('edit_pack', q.id)

    return render(request, 'add_pack.html')

def edit_pack(request, id):

    pack = get_object_or_404(QuizPack, id = id)

    if request.method == 'POST':

        try:
            pack_name = request.POST['name']
            category = request.POST['category']
        except:
            return render(request, 'edit_pack.html', {'failed' : True})

        pack.name = pack_name

        try:
            description = request.POST['description']
            pack.description = description
        except:
            pass

        pack.category = category
        pack.save()
        return redirect('edit_pack', pack.id)

    return render(request, 'edit_pack.html', {'pack' : pack, 'current_course_id' : request.session['current_course_id']})

def delete_pack(request, id):
    pack = get_object_or_404(QuizPack, id = id)
    pack.deltete()
    return redirect('edit_course', request.session['current_course_id'])

def add_question(request, id):
    pack = get_object_or_404(QuizPack, id = id)
    
    if request.method == "POST":

        try:
            question = request.POST['question']
            answer = request.POST['answer']
        except:
            return render(request, 'add_question.html', {'failed' : True, 'packid' : id})
        
        try:
            hint = request.POST['hint']
        except:
            hint = None
        
        q = Question.objects.create(question = question, answer = answer, hint = hint, pack = pack)
        q.save()

        return render(request, 'add_question.html', {'success' : True, 'packid' : id})

    return render(request, 'add_question.html', {'packid' : id})

def edit_question(request, id):
    question = get_object_or_404(Question, id = id)
    
    if request.method == "POST":

        try:
            questionin = request.POST['question']
            answerin = request.POST['answer']
        except:
            return render(request, 'edit_question.html', {'failed' : True})
        question.question = questionin
        question.answer = answerin
        
        try:
            hint = request.POST['hint']
            question.hint = hint
        except:
            pass
        question.save()

        return redirect('edit_pack', question.pack.id)

    return render(request, 'edit_question.html', {'question' : question, 'packid': question.pack.id})


def delete_question(request, id):
    question = get_object_or_404(Question, id = id)
    question.delete()
    return redirect('edit_pack', question.pack.id)

def register_pack(user, packid):
    pack = get_object_or_404(QuizPack, id=packid)
    if user in pack.registered_user.all():
        return
    pack.registered_user.add(user)

    for question in pack.question_set.all():
        QuestionSchedule.objects.create(user = user, question = question, scheduled_time=now(), previous_interval=DEFAULT_INTERVAL)

def unregister_pack(user, packid):
    pack = get_object_or_404(QuizPack, id=packid)
    if not user in pack.registered_user.all():
        return
    pack.registered_user.remove(user)

    for questionschedule in QuestionSchedule.objects.filter(user = user, question__pack = pack):
        questionschedule.delete()
