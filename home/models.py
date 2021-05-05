from django.db import models
from user.models import QUser

# Create your models here.
class Courses(models.Model):
    courseName = models.CharField(max_length = 50)
    beginDate = models.DateTimeField(auto_now_add=True)
    manageTeacher = models.ForeignKey(QUser, on_delete = models.CASCADE)

    def __str__(self):
        return className