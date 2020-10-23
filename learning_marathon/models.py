from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    now_learning = models.BooleanField(default=False)
    theory = models.BooleanField(default=False)

class LearningSession(models.Model):
    sessionId = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='progress')
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField(default=now)
    theory = models.BooleanField(default=True)

    def duration(self):
        return self.end_date - self.start_date

    def __str__(self):
        return f'{self.user} - learning session'
