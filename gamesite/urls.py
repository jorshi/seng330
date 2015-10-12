from django.conf.urls import patterns, include, url
from django.contrib import admin
import player.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gamesite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
   
    url(r'^$', player.views.home),
    url(r'^home/$', player.views.home),
    url(r'^login/$', player.views.login),
    url(r'^logout/$', player.views.player_logout),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', player.views.register),
    url(r'^accounts/login/$', player.views.login),
)
