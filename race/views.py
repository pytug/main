# creating views for the race app

from django.http import HttpResponse
from django.shortcuts import render
from race.models import User, Session

# index view, show last 5 sessions
def index(request):
    latest_session_list = Session.objects.order_by('-date')[:5]

#not quite yet needed
#    users = User.objects.all()
    
    context = { 'latest_session_list': latest_session_list }
    return render(request, 'race/index.html', context)

def user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404
    return render(request, 'race/user.html', {'user': user})
