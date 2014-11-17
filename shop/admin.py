from django.contrib import admin
from skillup.shop.models import *

# Register your models here.
admin.site.register(TrialSubscription, admin.ModelAdmin)
admin.site.register(CustomerBillingData, admin.ModelAdmin)
