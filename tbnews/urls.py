from django.conf.urls import patterns, include, url
from views import NewsItemCreateView, NewsItemDetailView, NewsItemListView, NewsItemUpdateView



urlpatterns = patterns('tbnews.views',
                       # url(r'^add/?$', 'addlocation', name='addlocation'),
                       # url(r'^add/?$', LocationCreate.as_view(), name='addlocation'),
                       url(r'^add/?$', NewsItemCreateView.as_view(), name='add_news_item'),
                       url(r'^update/(?P<pk>\d+)/?$', NewsItemUpdateView.as_view(), name='update_news_item'),
                       url(r'^$', NewsItemListView.as_view(), name='list_news_items'),
                       url(r'^detail/(?P<pk>\d+)/?$', NewsItemDetailView.as_view(), name='detail_news_item'),
                       )
