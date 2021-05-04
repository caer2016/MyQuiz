from django.db import models
from django.contrib.auth.models import User

class QUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name