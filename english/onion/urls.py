# coding=utf-8
import settings
from django.conf.urls import patterns, include, url

mainpath = 'src'

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_URL}),    
)

urlpatterns += patterns(mainpath + '.views',
#    (r'^read/(?P<pk>[\w.]+)$', 'read'),
    (r'^$', 'read'),
    (r'^upload$', 'upload'),
    (r'^upload_txt$', 'upload_txt'),    
    (r'^word_mark$', 'word_mark'),    

)

