from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.default'),
    url(r'^permalink/(.*)/(.*)', 'main.views.permalink'),
    # url(r'^$', 'youtubeinsight.views.home', name='home'),
    # url(r'^youtubeinsight/', include('youtubeinsight.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admndocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'main.views.custom_404'
