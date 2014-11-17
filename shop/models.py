from django.db import models
from django.contrib.auth.models import User
from skillup.shop.utils import copytree
from django.conf import settings
from datetime import datetime, timedelta

class CustomerData(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    company = models.CharField(max_length=200, null=True)
    lhc_user = models.IntegerField(null=True)
    real_customer = models.BooleanField(default=False)

class CustomerBillingData(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    vat_number = models.CharField(max_length=30)
    plan = models.CharField(max_length=100)
    agents = models.IntegerField(max_length=100,default=0)
    payment_months = models.CharField(max_length=100)

    def create(self, user):
        self.user = user
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.save()
        return self

class TrialSubscription(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    created_at = models.DateTimeField(null=True)
    ends_at = models.DateTimeField(null=True)

    def create(self, user):
        self.user = user
        self.created_at = datetime.today()
        self.ends_at = datetime.today() + timedelta(days=15)
        self.save()
        return self 

    def is_trialing(self, user):
        try:
            trial = TrialSubscription.objects.get(user__id=user.id)
            return trial
        except Exception:
            return False

