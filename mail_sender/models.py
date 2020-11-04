from django.db import models
from django.db.models.fields import CharField

class SentMail(models.Model):
    to = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    seconds = models.PositiveIntegerField()
    creation_time = models.DateTimeField(blank=True, null=True)
    sending_time = models.DateTimeField(blank=True, null=True)
