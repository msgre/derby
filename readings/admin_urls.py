from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .admin_views import AdminView, AdminRedirectView

urlpatterns = patterns('',
    url(r'^(?P<year_from>\d{4})-(?P<year_to>\d{4})/(?P<month>\d{1,2})/$', login_required(AdminView.as_view()), name="admin_month"),
    url(r'^$', login_required(AdminRedirectView.as_view()), name="admin_redir"),
)
