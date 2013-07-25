from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'chrome.views.home', name='home'),
    url(r'^process_command/', 'chrome.views.process_command', name='process_command'),
    url(r'^texttospeech/','chrome.views.textToSpeechTest', name='textToSpeech_test')
    # url(r'^jarvis/', include('jarvis.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
