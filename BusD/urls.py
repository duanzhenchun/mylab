from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

mainpath = 'BusD.src'

urlpatterns = patterns('',
    # Example:
    # (r'^BusD/', include('BusD.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns(mainpath,
    (r'^need/$', 'dealer.need_view'),
    (r'^feed/$', 'dealer.feed_view'),
    (r'^init/$', 'dealer.init_view'),
)
