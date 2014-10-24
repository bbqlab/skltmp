from django.contrib.auth.models import User
from django.db.models.signals import post_save
from skillup.shop.models import *
from .tasks import deploy_lhc

def install_chat_software(sender, **kwargs):
    print "post save"
    print kwargs
    if kwargs['created']:
        #subscription = Subscription().create(kwargs['instance'], plan)
        print "SENDING SIGNAL"
        deploy_lhc.apply_async([kwargs['instance'].id, 
                                      kwargs['instance'].username, 
                                      kwargs['instance'].password,
                                      "test"])


def initialize_installation(sender, **kwargs):
    trial = TrialSubscription().create(kwargs['instance'])
    install_chat_software(sender, **kwargs)

post_save.connect(initialize_installation, sender=User, weak=False, dispatch_uid='user_registration')


