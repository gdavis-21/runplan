from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils import timezone

class Goal(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    isComplete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.date}, {self.user}"

class Workout(models.Model):
    distance = models.IntegerField()
    effort = models.IntegerField()
    strengthCircuit = ArrayField(models.CharField(max_length=200), default=list)
    mobilityChallenge = ArrayField(models.CharField(max_length=200), default=list)
    strengthChallenge = ArrayField(models.CharField(max_length=200), default=list)
    videos = ArrayField(models.CharField(max_length=200), default=list)
    user = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return f"{self.distance}, {self.effort}, {self.user}"

class Race(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    isPast = models.BooleanField(default=False)

    def check_is_past(self):
        return self.date > timezone.now()

    def __str__(self):
        return f"{self.name}, {self.date}"