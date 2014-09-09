from django.conf.urls.defaults import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_URL}),
    # Example:
    # (r'^accountindex/', include('accountindex.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$', 'src.views.home'),
    (r'^download/$', 'src.views.download'),
    (r'^words/$', 'src.views.chart'),
)
