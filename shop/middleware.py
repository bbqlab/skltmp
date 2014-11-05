from django.conf import settings
from django.http import HttpResponseRedirect
from skillup.shop.forms import *
from mezzanine.accounts.forms import LoginForm

class UserCookieMiddleWare(object):
    """
    Middleware to set user cookie
    If user is authenticated and there is no cookie, set the cookie,
    If the user is not authenticated and the cookie remains, delete it
    """

    def process_response(self, request, response):
        #if user and no cookie, set cookie
        if request.user.is_authenticated() and not request.COOKIES.get('userId'):
            response.set_cookie("userId", '1',domain=settings.SESSION_COOKIE_DOMAIN)
        elif not request.user.is_authenticated() and request.COOKIES.get('userId'):
            #else if if no user and cookie remove user cookie, logout
            response.delete_cookie("userId", domain=settings.SESSION_COOKIE_DOMAIN)
        return response

class AgentLoginFormMiddleware(object):
    def process_request(self, request):
        agent_form = AgentLoginForm()
        login_form = LoginForm()

        request.agent_login_form = agent_form
        request.main_login_form = login_form