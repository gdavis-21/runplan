from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from runplan.models import Goal, Workout

def index(request):
    """
    Purpose: Redirects user to the login page (if not authenticated), or redirect to dashboard.
    Params:
        request: (HttpRequest) - An HttpRequest object.
    Returns:
        (HttpResponseRedirect) - Redirects to the login page or to the dashboard page.
    """
    if request.user.is_authenticated:
        url = reverse("dashboard")
        return HttpResponseRedirect(url)
    else:
        url = reverse("login")
        return HttpResponseRedirect(url)


def authenticate(request):
    """
    Purpose: Authenticates a user's login credentials. Attaches a session to the user's instance.
    Params:
        request: (HttpRequest) - An HttpRequest object.
    Returns: 
        (HttpResponse) - On successful authentication, returns a HttpResponse with code 200
        (HttpResponse) - On failed authentication, returns a HttpResponse with error code 403.
    """ 
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponse("Success", status=200)
        else:
            # User did not enter successful 'username' / 'password' combination
            return HttpResponse("Unauthorized", status=403)
    else:
        # Request's method is not "POST"
        return HttpResponse("Unauthenticated", status=403)
    
def fetchUserData(request):
    """
    Purpose: Fetch user data (workouts, goals) from DB.
    Params:
        request: (HttpRequest) - An HttpRequest object.
    Returns: (JsonResponse) - Returns a JSON object with user's workouts and goals.
    e.g. {
    "workouts": [
        {
        ...
        },
        {
        ...
        }
        ...
    ],
    "goals": [
        {
        ...
        },
        {
        ...
        },
        {
        ...
        }
    ]
    }
    """
    if request.method == "GET":
        if request.user.is_authenticated:
            goals = [goal.toDictionary() for goal in (Goal.objects.filter(user=request.user))]
            workouts = [workout.toDictionary() for workout in (Workout.objects.filter(user=request.user))]
            return JsonResponse({
                "goals": goals,
                "workouts": workouts
            }   ,safe=False)
        else:
            # User is not authenticated.
            return HttpResponse("Unauthenticated", stauts=403)
