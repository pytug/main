# creating views for the pyramid app

from django.http import HttpResponse
#from django.views.generic.dates import YearArchiveView
from pyramid.models import Session
from django.shortcuts import render

def index(request):
    latest_session_list = Session.objects.order_by('-date')[:5]
#    template = loader.get_template('pyramid/index.html')
    context = { 'latest_session_list': latest_session_list }
    return render(request, 'pyramid/index.html', context)


def detail(request, session_id):
    return HttpResponse("You're looking at session %s." % session_id)

def results(request, session_id):
    return HttpResponse("You're looking at the results of session %s." % session_id)

def vote(request, session_id):
    return HttpResponse("You're voting on session %s." % session_id)

#class SessionYearArchiveView(YearArchiveView):
#    queryset = Session.objects.all()
#    date_field = "date"
#    make_object_list = True
#    allow_future = True
