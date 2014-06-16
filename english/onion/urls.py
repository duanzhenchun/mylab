# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()
mainpath = 'src'


urlpatterns = patterns('',
    (r'^accounts/', include('allauth.urls')),
    url(r'accounts/login/$', TemplateView.as_view(template_name='login/index.html')),
    url(r'^accounts/profile/$', TemplateView.as_view(template_name='login/profile.html')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^captcha/', include('captcha.urls')),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns(mainpath + '.views',
    (r'^$', 'read'),
    (r'^upload$', 'upload'),
    (r'^upload_txt$', 'upload_txt'),    
    (r'^word_mark$', 'word_mark'),    
    (r'^mywords$', 'mywords'),    
    (r'^word_repeat$', 'word_repeat'),    
)

