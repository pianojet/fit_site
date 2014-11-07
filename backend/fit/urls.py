from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from fit.accounts.api import UserResource, UserProfileResource

admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(UserProfileResource())


urlpatterns = patterns('',
	url(r'^login/', 'fit.accounts.views.login', name='accounts_login'),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
