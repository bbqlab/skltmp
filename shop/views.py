from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, Context
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from skillup.shop.forms import *
from chargify.models import *
import logging


@login_required
def profile(request):
    trial = TrialSubscription().is_trialing(request.user)

    #TODO: get real chargify subscritpion
    if not trial:
        pass
        
    return render_to_response('shop/profile.html', {'user': request.user, 'trial': trial}, 
            context_instance=RequestContext(request))

@login_required
def change_plan(request):
    return render_to_response('shop/change_plan.html', {'user': request.user}, 
            context_instance=RequestContext(request))

@login_required
def invoices(request):
    return render_to_response('shop/invoices.html', {'user': request.user}, 
            context_instance=RequestContext(request))

@login_required
def checkout(request):
    try:
        billing_data = CustomerBillingData.objects.get(user_id=request.user.id)
    except Exception,e:
        billing_data = CustomerBillingData().create(request.user)

    if request.GET:
        subscription_info = {'agents': request.GET['agents'],
                                                'plan': request.GET['plan'],
                                                'payment_months': request.GET['payment_months']}
        billing_form = BillingDataForm(instance=billing_data,
                                       initial=subscription_info)
    else:
        subscription_info = {'agents': request.POST['agents'],
                             'plan': request.POST['plan'],
                             'payment_months': request.POST['payment_months']}
        billing_form = BillingDataForm(request.POST, instance=billing_data)


    #TODO: init form with chargify data
    cc_form = CreditCardForm()
    handle = "%s-%s-month" % (subscription_info['plan'], subscription_info['payment_months'])
    product = Product.objects.get(handle=handle)
    agents_component = Component.objects.get(product_family_id=product.product_family_id)

    subscription_info['unit_price'] = agents_component.unit_price
    subscription_info['price'] = int(agents_component.unit_price) * int(subscription_info['agents'])
    
    if request.POST and billing_form.is_valid():
        
        billing_form.save()
        
        
        components = [{'component': agents_component, 'quantity': billing_form.cleaned_data['agents']}]
        url = product.get_hosted_page_url(components, request.user)


        #redirect to hosted page
        #TOFIX: url generico

        url = "https://bbqlab.chargify.com/h/%s/subscriptions/new" % (product.chargify_id)
        url = "%s?ref=%s&components[][component_id]=%s&components[][allocated_quantity]=%s" % (url, request.user.id, agents_component.chargify_id, billing_form.cleaned_data['agents'])

        return HttpResponseRedirect(url)
    else:

        return render_to_response('shop/checkout.html', {'user': request.user, 
                                                         'cc_form':cc_form, 
                                                         'info': subscription_info, 
                                                         'billing_form': billing_form}, 
                                   context_instance=RequestContext(request))

@login_required
def billing_info(request):
    try:
        billing_data = CustomerBillingData.get(user_id=request.user.id)
    except Exception,e:
        billing_data = CustomerBillingData().create(request.user)
        
    billing_form = BillingDataForm(request.POST or None,
         instance=billing_data)
    
    if request.POST:
        if billing_form.is_valid():
            billing_form.save()

    return render_to_response('shop/billing_info.html', {'user': request.user, 'form': billing_form}, 
            context_instance=RequestContext(request))

@login_required
def chargify_signup(request):
    customer = Customer.objects.get_or_load(request.GET['customer_id'])
    customer.save()

    subscription = Subscription.objects.get_or_load(request.GET['id'])
    subscription.customer = customer
    subscription.save()
    
    return HttpResponseRedirect('/shop/payment?status=success')

@login_required
def payment(request):
    status = 'error'

    if request.GET:
        status = request.GET['status']

    return render_to_response('shop/payment.html', {'user': request.user, 'status': status}, 
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
    import logging
    logger = logging.getLogger(__name__)
    logger.debug("settings")

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
