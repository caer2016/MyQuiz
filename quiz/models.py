from django.db import models
from django.contrib.auth.models import User

class QuizPack(models.Model):

    name = models.CharField(max_length = 50)
    description = models.TextField()
    category = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

class Question(models.Model):

    question = models.TextField()
    hint = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question 

class Student(models.Model):

    user = models.OneToOneField(User, null = False, on_delete = models.CASCADE)
    question_schedules = models.ManyToManyField(Question)