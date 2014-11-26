from django.conf.urls import patterns, url
from .views import MonthlyReadingsView, YearlyReadingsView

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2}).html$', MonthlyReadingsView.as_view(), name='readings_monthly'),
    url(r'^(?P<year_start>\d{4})-(?P<year_end>\d{4}).html$', YearlyReadingsView.as_view(), name='readings_yearly'),
)
