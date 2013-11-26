from django.conf.urls import patterns, include, url
from views import NewsItemCreateView, NewsItemDetailView, NewsItemListView, NewsItemUpdateView, NewsItemDeleteView



urlpatterns = patterns('tbnews.views',
                       # url(r'^add/?$', 'addlocation', name='addlocation'),
                       # url(r'^add/?$', LocationCreate.as_view(), name='addlocation'),
                       url(r'^(?P<kind>loc|org)-(?P<obj_id>\d+)/add/?$', NewsItemCreateView.as_view(),name='add_news_item'),
                       # url(r'^org-(?P<obj_id>\d+)/add/?$', NewsItemCreateView.as_view(kind="organization"),name='add_org_news_item'),

                       url(r'^(?P<kind>loc|org)-(?P<obj_id>\d+)/update/(?P<pk>\d+)/?$', NewsItemUpdateView.as_view(), name='update_news_item'),
                       # url(r'^org-(?P<obj_id>\d+)/update/(?P<pk>\d+)/?$', NewsItemUpdateView.as_view(kind="organization"), name='update_news_item'),


                       url(r'^(?P<kind>loc|org)-(?P<obj_id>\d+)$', NewsItemListView.as_view(), name='list_news_items'),
                       # url(r'^org-(?P<obj_id>\d+)$', NewsItemListView.as_view(kind="organization"), name='list_org_news_items'),

                       url(r'^(?P<kind>loc|org)-(?P<obj_id>\d+)/detail/(?P<pk>\d+)/?$', NewsItemDetailView.as_view(), name='detail_news_item'),
                       # url(r'^org-(?P<obj_id>\d+)/detail/(?P<pk>\d+)/?$', NewsItemDetailView.as_view(kind="organization"), name='detail_news_item'),

                       url(r'^(?P<kind>loc|org)-(?P<obj_id>\d+)/remove/(?P<pk>\d+)/?$', NewsItemDeleteView.as_view(), name='delete_news_item'),
                       # url(r'^org-(?P<obj_id>\d+)/remove/(?P<pk>\d+)/?$', NewsItemDeleteView.as_view(kind="organization"), name='delete_news_item'),
                       )
