from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.gis import admin
from filebrowser.sites import site


from views import MyConnectionsView, UserProfileFormView

admin.autodiscover()

urlpatterns = patterns('',

    (r'^accounts/', include('allauth.urls')),
    (r'^avatar/', include('avatar.urls')),
    url(r'^accounts/profile/?$', MyConnectionsView.as_view(), name='user_dashboard'),
    url(r'^accounts/update/?$', UserProfileFormView.as_view(), name='user_profile_update'),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^$', 'thoughtbubble.views.home', name='home'),

    url(r'^signup/?$', 'thoughtbubble.views.signup', name='signup'),

    # url(r'^accounts/profile/?$', 'thoughtbubble.views.dashboard', name='user_dashboard'),

    url(r'^supporting/', include('ideation.supportering.urls')),

    url(r'^login/?$', 'thoughtbubble.views.login', name='login'),
    url(r'^logout/?$', 'thoughtbubble.views.logout', name='logout'),

    (r'^admin/filebrowser/', include(site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    # url(r'^admin$', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
    url(r'^', include('thoughtbubble.geo_urls')),
    url(r'^news/', include('tbnews.urls')),

    url(r'^checkout/?$', 'thoughtbubble.views.checkout', name='checkout'),
    url(r'^checkout-thanks/?$', 'thoughtbubble.views.debit_card', name='post_checkout'),
    # url('', include('social.apps.django_app.urls', namespace='social')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('', url('', include('django.contrib.flatpages.urls')),)
