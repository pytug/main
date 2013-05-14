# creating views for the race app

from django.http import HttpResponse
from django.shortcuts import render
from race.models import User, Session

# index view, show last 5 sessions
def index(request):
    latest_session_list = Session.objects.order_by('-date')[:5]
    context = { 'latest_session_list': latest_session_list }
    return render(request, 'race/index.html', context)
