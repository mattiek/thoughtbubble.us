from django.conf.urls import patterns, include, url

urlpatterns = patterns('ideation.supportering.views',
                       url(r'^comment/(?P<id>\d+)/?$', 'support_comment', name='support_comment'),
                       )
