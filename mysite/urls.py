from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from mysite.core import views as core_views
from mysite.core.api import urls as api_urls
admin.autodiscover()


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-devices/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(api_urls, namespace="api")),
]
