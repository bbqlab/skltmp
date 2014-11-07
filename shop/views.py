from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from skillup.shop.forms import *


def profile(request):
    return render_to_response('shop/profile.html', {'user': request.user}, 
            context_instance=RequestContext(request))

def change_plan(request):
    return render_to_response('shop/change_plan.html', {'user': request.user}, 
            context_instance=RequestContext(request))

def invoices(request):
    return render_to_response('shop/invoices.html', {'user': request.user}, 
            context_instance=RequestContext(request))

def billing_info(request):
    return render_to_response('shop/billing_info.html', {'user': request.user}, 
            context_instance=RequestContext(request))

def agent_login(request):
    form = AgentLoginForm()
    not_found = False
    if request.method == 'POST':
        form = AgentLoginForm(request.POST) # Bind data from request.POST into a PostForm
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['skillup_id']).count():
                path = "%s%s" % (settings.LHC_DASHBOARD_URL, form.cleaned_data['skillup_id'])
                return HttpResponseRedirect(path)
            else:
                not_found = True


 
    return render(request, 'shop/agent_login.html', {
        'form': form,
        'not_found': not_found
    })

def goto_account(request):
    path = '/'
    if request.user.is_authenticated():
        path = "%s%s" % (settings.LHC_DASHBOARD_URL, request.user.username)
    return HttpResponseRedirect(path)

def goto_dashboard(request):
    path = '/'
    if request.user.is_authenticated():
        path = "%s%s" % (settings.LHC_DASHBOARD_URL, request.user.username)
    return HttpResponseRedirect(path)

def wait_lhc_install(request):
    return render_to_response('shop/wait_lhc_install.html', {'user': request.user}, 
            context_instance=RequestContext(request))
