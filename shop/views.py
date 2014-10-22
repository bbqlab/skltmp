from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext, Context
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404



def goto_dashboard(request):
    path = '/'
    if request.user.is_authenticated():
        path = "%s%s" % (settings.LHC_DASHBOARD_URL, request.user.username)
    return HttpResponseRedirect(path)

def wait_lhc_install(request):
    return render_to_response('shop/wait_lhc_install.html', {'user': request.user}, 
            context_instance=RequestContext(request))