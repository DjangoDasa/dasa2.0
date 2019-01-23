from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.db import models


# Create your models here.
class Analysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analysis')

    analysis = models.CharField(max_length=8192, default='Null')

    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def __repr__(self):
        return '<Analysis: {}>'.format(self.analysis)

    def __str__(self):
        return '{}'.format(self.analysis)
