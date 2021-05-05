from django.db import models
from django.contrib.auth.models import User

class QuizPack(models.Model):

    name = models.CharField(max_length = 50, null = False)
    description = models.TextField(null = True)
    category = models.CharField(max_length = 20, null = False)

    def __str__(self):
        return self.name

class Question(models.Model):

    pack = models.ForeignKey(QuizPack, null = False, on_delete = models.CASCADE)
    question = models.TextField(null = False)
    hint = models.TextField(null = True)
    answer = models.TextField(null = False)

    def __str__(self):
        return self.question 

class QuestionSchedule(models.Model):

    user = models.ForeignKey(User, null = False, on_delete = models.CASCADE)
    question = models.ForeignKey(Question, null = False, on_delete = models.CASCADE)
    scheduled_time = models.DateTimeField(null = False)
    previous_interval = models.DurationField(null = False)