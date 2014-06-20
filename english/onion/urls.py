# coding=utf-8
import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


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
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns(mainpath + '.views',
    (r'^$', 'read'),
    (r'^read$', 'read'),
    (r'^lastpage$', 'lastpage'),
    (r'^word_mark$', 'word_mark'),    
    (r'^word_known$', 'word_known'),    
    (r'^word_unknown$', 'word_unknown'),    
    (r'^word_repeat$', 'word_repeat'),    
    (r'^word_save$', 'word_save'),    
)

