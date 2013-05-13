# the URLconf file for race app

from django.conf.urls import patterns, url

from race import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)

