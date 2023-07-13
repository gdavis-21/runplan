from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.http import JsonResponse
from runplan.models import Goal, Workout

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            goals = [goal.toDictionary() for goal in (Goal.objects.filter(user=user))]
            workouts = [workout.toDictionary() for workout in (Workout.objects.filter(user=user))]
            return JsonResponse({
                "goals": goals,
                "workouts": workouts
            }   ,safe=False)
        else:
            # User did not enter successful 'username' / 'password' combination
            return HttpResponse("Error")

