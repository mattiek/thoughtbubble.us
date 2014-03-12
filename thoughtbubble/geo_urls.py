from django.conf.urls import patterns, include, url

# urlpatterns = patterns('',
#     url(r'^(?P<state>\w+)/(?P<city>[-%\w ]+)/?$', 'thoughtbubble.views.home', name='home'),
#     url(r'^(?P<state>\w+)/(?P<city>[-%\w ]+)/ideas/', include('idea.urls')),
#     url(r'^(?P<state>\w+)/(?P<city>[-%\w ]+)/locations/', include('location.urls')),
#     url(r'^(?P<state>\w+)/(?P<city>[-%\w ]+)/organizations/', include('organization.urls')),
#     url(r'^(?P<state>\w+)/(?P<city>[-%\w ]+)/neighborhoods/', include('neighborhood.urls')),
#     url(r'^(?P<state>\w+)/(?P<city>\w+)/explore/?$', 'thoughtbubble.views.explore', name='explore'),
#     url(r'^(?P<state>\w+)/(?P<city>\w+)/explore/(?P<pk>\d+)/?$', 'thoughtbubble.views.sherlock', name='sherlock'),
#     )


urlpatterns = patterns('',
   url(r'^$', 'thoughtbubble.views.home', name='home'),
   url(r'^geo/ideas/', include('ideation.idea.urls')),
   url(r'^geo/locations/', include('geo.location.urls')),
   # url(r'^cities/', include('geo.cities.urls')),
   url(r'^geo/organizations/', include('geo.organization.urls')),
   url(r'^geo/places/', include('geo.places.urls')),
   url(r'^geo/explore/?$', 'thoughtbubble.views.explore', name='explore'),
   url(r'^geo/explore/(?P<place>[\w-]+)/(?P<organization>[\w-]+)/?$', 'thoughtbubble.views.sherlock', name='sherlock'),
   )