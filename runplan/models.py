from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from datetime import datetime

class Goal(models.Model):
    name = models.CharField(max_length=200)
    isComplete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.user}"

    def toDictionary(self):
        return {
            "name": self.name,
            "isComplete": self.isComplete
        }
    
class Workout(models.Model):
    date = models.DateField(default=datetime.now)
    distance = models.CharField(max_length=200)
    pace = models.CharField(max_length=200)
    strengthCircuit = ArrayField(models.CharField(max_length=200), default=list)
    mobilityChallenge = ArrayField(models.CharField(max_length=200), default=list)
    videos = ArrayField(models.CharField(max_length=200), default=list)
    user = models.ForeignKey(User, models.CASCADE)

    def __str__(self):
        return f"{self.distance}, {self.pace}, {self.user}"
    
    def toDictionary(self):
        return {
            "date": self.date.isoformat(),
            "distance": self.distance,
            "effort": self.pace,
            "strengthCircuit": self.strengthCircuit,
            "mobilityChallenge": self.mobilityChallenge,
            "videoURLS": self.videos
        }

class Race(models.Model):
    date = models.DateField(default=datetime.now)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} - {self.date}"
    
    def toDictionary(self):
        return {
            "date": self.date.isoformat(),
            "name": self.name
        }

