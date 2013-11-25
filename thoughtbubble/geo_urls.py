from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<state>\w+)/(?P<city>[-%\w ]+)/?$', 'thoughtbubble.views.home', name='home'),
    url(r'^(?P<state>\w+)/(?P<city>[-%\w ]+)/ideas/', include('idea.urls')),
    url(r'^(?P<state>\w+)/(?P<city>[-%\w ]+)/locations/', include('location.urls')),
    url(r'^(?P<state>\w+)/(?P<city>[-%\w ]+)/organizations/', include('organization.urls')),
    url(r'^(?P<state>\w+)/(?P<city>[-%\w ]+)/neighborhoods/', include('neighborhood.urls')),
    url(r'^(?P<state>\w+)/(?P<city>\w+)/explore/?$', 'thoughtbubble.views.explore', name='explore'),
    url(r'^(?P<state>\w+)/(?P<city>\w+)/explore/(?P<pk>\d+)/?$', 'thoughtbubble.views.sherlock', name='sherlock'),
    )