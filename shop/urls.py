from django.conf.urls import patterns, url, include
from skillup.shop.views import *


urlpatterns = patterns('',
    url(r"^gotodashboard/$", goto_dashboard),
    url(r"^profile/$", profile, name='profile'),
    url(r"^changeplan/$", change_plan, name='change_plan'),
    url(r"^invoices/$", invoices, name='invoices'),
    url(r"^billing/$", billing_info, name='billing'),
    url(r"^agentlogin/$", agent_login, name='agentlogin'),
    url(r"^gotoaccount/$", goto_account),
    url(r"^wait/$", wait_lhc_install)
)
