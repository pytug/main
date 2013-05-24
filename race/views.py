# creating views for the race app

from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from race.models import User, Session
from django.db.models import Max
from django.http import Http404

# index view, show last 5 sessions
def index(request):
    latest_session_list = Session.objects.order_by('-date')[:10]
    template = loader.get_template('race/index.html')
    context = Context({
        'latest_session_list': latest_session_list 
    })
    return HttpResponse(template.render(context))

def user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_session_count = user.session_set.count()
        user_session_list = Session.objects.filter(user_id=user_id).order_by('-date')
        user_session_max = user_session_list.aggregate(Max('reps'))
        template = loader.get_template('race/user.html')
        context = Context({
            'user_session_list': user_session_list,
            'user': user,
            'user_session_count': user_session_count,
            'user_session_max': user_session_max,
        })
    except User.DoesNotExist:
        raise Http404
    return HttpResponse(template.render(context))

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.template import RequestContext
from django import template

def action(request):
    msg = "empty"
    try:
        user_list = User.objects.all()
        template = loader.get_template('race/action.html')
        selected_user = 1
        reps_done = 0
        if "user" in request.POST and "reps" in request.POST:
            selected_user =  request.POST["user"]
            reps_done = request.POST["reps"]
        context = RequestContext(request, {
            'user_list': user_list,
            'selected_user': selected_user,
            'reps_done': reps_done,
        })
        if int(reps_done) > 0:
            s = Session(date=timezone.now(), user_id=selected_user, reps=reps_done)
            s.save()
            return HttpResponseRedirect(reverse('index'))
    except ValueError:
        msg = "value error"
    return HttpResponse(template.render(context))

def topusers(request):
    user_max_list = []
    user_list = User.objects.all()
    for user in user_list:
        user_session_list = Session.objects.filter(user_id=user.id)
        user_session_max = { user_session_list.aggregate(Max('reps'))['reps__max']: user.name }
        user_max_list.append(user_session_max)
    user_max_list = sorted(user_max_list, reverse=True)[:3]
    template = loader.get_template('race/topusers.html')
    context = Context({
        'user_max_list': user_max_list,
    })
    return HttpResponse(template.render(context))

