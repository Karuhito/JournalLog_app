from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Journal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return F"{self.user.username} - {self.date}"

class Goal(models.Model):
    title = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Todo(models.Model):
    title = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
