from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from ratings.api import CategoryResource, RatingResource

admin.autodiscover()

v1_api = Api(api_name="v1")
v1_api.register(CategoryResource())
v1_api.register(RatingResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^category/$', 'ratings.views.index'),
    url(r'^category/(?P<category_id>\d+)/$', 'ratings.views.detail'),
    url(r'^category/(?P<category_id>\d+)/rate/$', 'ratings.views.rate'),
)
