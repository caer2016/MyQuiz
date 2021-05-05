from django.db import models
from django.contrib.auth.models import User
from quiz.models import QuizPack

# class QUser(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='quser')

#     @property
#     def get_name(self):
#         return self.user.first_name + " " + self.user.last_name

#     @property
#     def get_instance(self):
#         return self

#     def __str__(self):
#         return self.user.last_name

class Courses(models.Model):
    courseName = models.CharField(max_length=50)
    beginDate = models.DateTimeField(auto_now_add=True)
    manageTeacher = models.ForeignKey(User, on_delete = models.CASCADE)
    student = models.ManyToManyField(User, related_name='student')
    required = models.ManyToManyField(QuizPack, related_name='required')

    def __str__(self):
        return self.courseName