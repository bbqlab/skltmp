from django.conf.urls import patterns, url, include
from skillup.shop.views import *


urlpatterns = patterns('',
    url(r"^gotodashboard/$", goto_dashboard),
    url(r"^wait/$", wait_lhc_install)
)
