# creating views for the race app

from django.http import HttpResponse
from django.template import Context, loader
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
        user_session_count = user.session_set.count()
        user_session_list = Session.objects.filter(user_id=user_id).order_by('-date')
        template = loader.get_template('race/user.html')
        context = Context({
            'user_session_list': user_session_list,
            'user': user,
            'user_session_count': user_session_count,
        })
    except User.DoesNotExist:
        raise Http404
    return HttpResponse(template.render(context))
