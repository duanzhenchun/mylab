# coding=utf-8
import settings
from django.conf.urls import patterns, include, url

mainpath = 'src'

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_URL}),    
)

urlpatterns += patterns(mainpath + '.views',
    (r'^read$', 'read'),
    (r'^upload$', 'upload'),
    (r'^upload_txt$', 'upload_txt'),    
)

