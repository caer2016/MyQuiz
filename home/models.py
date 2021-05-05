from django.db import models
from user.models import QUser

# Create your models here.
class ClassModel(models.Model):
    classID = models.CharField(max_length=20)
    className = models.CharField(max_length=20, null=False, default=None)
    manageTeacher = models.ForeignKey(QUser, on_delete=models.CASCADE)
    beginDate = models.DateTimeField(auto_now_add=True)

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return className