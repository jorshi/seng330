from django.conf.urls import patterns, include, url
from django.contrib import admin
import player.views
import gamesite.views
import gamesite.settings

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', player.views.home, name='home'),
    url(r'^login/$', player.views.login_register, {'tab': 'login'}, name='login'),
    url(r'^accounts/login/$', player.views.login_register, {'tab': 'login'}), # use with @login_required
    url(r'^logout/$', player.views.player_logout, name='logout'),
    url(r'^register/$', player.views.login_register, {'tab': 'register'}, name='register'),

)

# Serve Doxygen static files in development #TODO look into serving for production
if gamesite.settings.DEBUG:
    urlpatterns += [
        url(r'^doxygen/(?P<path>.*)$',
        gamesite.views.doxygen,
    )]
