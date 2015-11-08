from django.conf.urls import patterns, include, url
from django.contrib import admin
import player.views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', player.views.home),
    url(r'^login/$', player.views.login),
    url(r'^accounts/login/$', player.views.login), # use with @login_required
    url(r'^logout/$', player.views.player_logout),
    url(r'^register/$', player.views.register),
    #url(r'^new_game/$', player.views.new_game),
    #url(r'^resume_game/$', player.views.resume_game),

)
