from django.conf.urls import patterns, include, url

from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'thoughtbubble.views.home', name='home'),
    url(r'^signup/?$', 'thoughtbubble.views.signup', name='signup'),
    url(r'^dashboard/?$', 'thoughtbubble.views.dashboard', name='user_dashboard'),
    url(r'^ideas/', include('idea.urls')),
    url(r'^locations/', include('location.urls')),
    url(r'^communities/', include('community.urls')),
    url(r'^login/?$', 'thoughtbubble.views.login', name='login'),
    url(r'^logout/?$', 'thoughtbubble.views.logout', name='logout'),
    url(r'^explore/?$', 'thoughtbubble.views.explore', name='explore'),
    url(r'^explore/(?P<state>\w+)/(?P<city>\w+)/(?P<pk>\d+)/?$', 'thoughtbubble.views.explore', name='explore'),
    url(r'^privacy-policy/?$', 'thoughtbubble.views.privacy', name='privacy'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.flatpages.urls')),
)

