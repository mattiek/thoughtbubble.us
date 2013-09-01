from django.conf.urls import patterns, include, url

from django.contrib.gis import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'thoughtbubble.views.home', name='home'),
    url(r'^signup/?$', 'thoughtbubble.views.signup', name='signup'),
    url(r'^ideas/', include('idea.urls')),
    url(r'^locations/', include('location.urls')),
    url(r'^logout/?$', 'thoughtbubble.views.logout', name='logout'),
    url(r'^explore/?$', 'thoughtbubble.views.explore', name='explore'),
    url(r'^privacy-policy/?$', 'thoughtbubble.views.privacy', name='privacy'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
)

