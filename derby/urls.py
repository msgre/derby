from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from common.views import HomepageView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/index.html')),
    url(r'^index.html$', HomepageView.as_view(), name='homepage'),
    url(r'^sezona/', include('readings.urls')),
    url(r'^administrace/', include('readings.admin_urls')),
    (r'^prihlaseni/$', 'django.contrib.auth.views.login', {'template_name': 'common/login.html'}),
    (r'^odhlaseni/$', 'django.contrib.auth.views.logout', {'next_page': '/index.html'}),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
