from django.conf.urls import patterns, include, url
from django.contrib import admin
import player.views
import gamesite.views
import gamesite.settings
import gamestate.views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # Player Views
    url(r'^$', player.views.home, name='home'),
    url(r'^login/$', player.views.login_register, {'tab': 'login'}, name='login'),
    url(r'^accounts/login/$', player.views.login_register, {'tab': 'login'}), # use with @login_required
    url(r'^logout/$', player.views.player_logout, name='logout'),
    url(r'^register/$', player.views.login_register, {'tab': 'register'}, name='register'),
    url(r'^qunit_tests/$', player.views.qunit_tests),
#    url(r'^delete_game/$', player.views.delete_game),

    # Gamestate Views
    url(r'^get_current_room/$', gamestate.views.get_current_room),
    url(r'^get_inventory/$', gamestate.views.get_inventory),
    url(r'^get_doors/$', gamestate.views.get_doors),
    url(r'^use_door/$', gamestate.views.use_door),
)

# Serve Doxygen static files in development #TODO look into serving for production
if gamesite.settings.DEBUG:
    urlpatterns += [
        url(r'^doxygen/(?P<path>.*)$',
        gamesite.views.doxygen,
    )]
