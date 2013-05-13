# the URLconf file for pyramid app

from django.conf.urls import patterns, url

from pyramid import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<session_id>\d+)/$', views.detail, name='detail'),
#    url(r'^(?P<session_id>\d+)/$', views.detail, name='detail'),
    # ex: /session/5/results/
    url(r'^(?P<session_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<session_id>\d+)/vote/$', views.vote, name='vote'),
#    url(r'^(?P<year>\d{4})/$',
#        SessionYearArchiveView.as_view(),
#        name="article_year_archive"),
)
