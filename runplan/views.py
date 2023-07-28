from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from runplan.models import Goal, Workout, Race
from datetime import datetime
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

def index(request):
    """
    Purpose: Redirects user to the login page (if not authenticated), or redirect to dashboard.
    Params:
        request: (HttpRequest) - An HttpRequest object.
    Returns:
        (HttpResponse) - If user is authenticated, returns a successful HttpResponse, else returns forbidden HttpResponse.
    """
    if request.user.is_authenticated:
        return HttpResponse("Success")
    else:
        return HttpResponse("Forbidden", status=403)


def authenticateUser(request):
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
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Success")
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
            response =  JsonResponse({
                "goals": goals,
                "workouts": workouts
            }   ,safe=False)
            return response
        else:
            response = HttpResponse("Unauthenticated", status=403)
            return response

def fetchUpcomingRaces(request):
    """
    Purpose: Fetch upcoming races from DB.
    Params:
        request: (HttpRequest) - An HttpRequest object.
    Returns: (JsonResponse) - Returns a JSON object with upcoming races.
    e.g. [
        {
            "name": ... (String object)
            "date": ... (Date object)
        },
        {
            "name": ... (String object)
            "date": ... (Date object)
        }
    """
    if request.method == "GET":
        now = datetime.now()
        upcomingRaces = [race.toDictionary() for race in Race.objects.filter(date__gte=now.date())]
        response = JsonResponse(
            upcomingRaces
        , safe=False)
        return response

def updateUserGoals(request):
    """
    Update a user's goals (includes creation of a goal) in the DB.
    Params: 
        request (HttpResponse) - HttpRequest (containing POST data)
    Returns: 
        HttpResponse 200 for success, else HttpResponse 403
    """
    if request.method == "POST" and request.user.is_authenticated:
        goals = Goal.objects.filter(user=request.user)
        for key in request.POST:
            goal = goals[int(key)]
            if request.POST[key] == "":
                goal.delete()
            else:
                goal.name = request.POST[key]
                goal.save()
        return HttpResponse()
    else:
        return HttpResponse("Unauthenticated", status=403)

def addUserGoal(request):
    """
    Adds a goal to the list of goals associated with a user.
    Params:
        request (HttpRequest) An HttpRequest object.
    Returns:
        On success, HttpResponse with successful status code (i.e. 200)
        On failure, HttpResponse with successful status code (i.e. 403)
    """
    if request.method == "POST" and request.user:
        goal = Goal(name="Example Goal", isComplete=False, user=request.user)
        goal.save()
        return HttpResponse()
    else:
        return HttpResponse("Unauthorized", status=403)

@ensure_csrf_cookie
def fetchCSRFToken(request):
    """
    Fetch the CSRF token associated with a user's session.
    Params: 
        request (HttpResponse) - An HttpRequest object.
    Returns: On success, a HttpResponse containing the CSRF token as a cookie.
             On failure, an HttpResponse object with status code 403.
    e.g.
    {
    "csrfToken": ....
    }
    """
    if request.method == "GET":
        response = HttpResponse("Success")
        # response.set_cookie('csrftoken', request.COOKIES['csrftoken'], samesite='None', secure=True)
        return response
    else:
        return HttpResponse("Unauthorized", status=403)