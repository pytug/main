# the URLconf file for race app

from django.conf.urls import patterns, url

from race import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<user_id>\d+)/$', views.user, name='user'),
#    url(r'^(?P<user_id>\d+)/users/$', views.user, name='user'),
)

