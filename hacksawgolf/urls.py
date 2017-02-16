from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('home.urls', namespace='home')),
    url(r'^login/', include('login.urls', namespace='login')),
    url(r'^register/', include('register.urls', namespace='register')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^tournament/', include('tournament.urls', namespace='tournament')),
    url(r'^team/', include('team.urls', namespace='team')),
    url(r'^league/', include('league.urls', namespace='league')),
    url(r'^rules/', include('rules.urls', namespace='rules')),
    (r'^tinymce/', include('tinymce.urls')),
)

'''
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
'''
