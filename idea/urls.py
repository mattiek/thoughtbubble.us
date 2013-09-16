from django.conf.urls import patterns, include, url

urlpatterns = patterns('idea.views',
   url(r'^add/?$', 'addidea', name='addidea'),
   url(r'^list/?$', 'listideas', name='listideas'),
)
