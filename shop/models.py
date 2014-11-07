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
