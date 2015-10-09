from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gamesite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #default url
    url(r'^$', 'gamesite.views.home'),

    #login urls
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^login/$', 'gamesite.views.login'),
    url(r'^invalid/$', 'gamesite.views.invalid_login'),
    url(r'^auth/$', 'gamesite.views.auth_view'),
    url(r'^loggedin/$', 'gamesite.views.loggedin'),
    url(r'^logout/$', 'gamesite.views.logout'),
    url(r'^home/$', 'gamesite.views.home')
                       
)

