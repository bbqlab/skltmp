from django import forms
from django.core.exceptions import ValidationError
from skillup.shop.models import *

class AgentLoginForm(forms.Form):
    skillup_id = forms.CharField(
        label="SkillUp ID",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            skillup_id = kwargs['instance'].skillup_id
            kwargs.setdefault('initial', {})['skillup_id'] = skillup_id

        return super(AgentLoginForm, self).__init__(*args, **kwargs)

class BillingDataForm(forms.ModelForm):
    plan = forms.CharField(required=False)
    agents = forms.CharField(required=False)
    payment_months = forms.CharField(required=False)

    class Meta:
        model = CustomerBillingData
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        super(BillingDataForm, self).__init__(*args, **kwargs)
        self.fields['agents'].widget = HiddenInput()
        self.fields['payment_months'].widget = HiddenInput()
        self.fields['plan'].widget = HiddenInput()

class CreditCardForm(forms.Form):
    number = forms.CharField(label='Numero di carta')
    cvv = forms.CharField(label='CVV')
    expiration_month = forms.IntegerField(label='Mese')
    expiration_year = forms.IntegerField(label='Anno')
    name = forms.CharField(label='Nome')
    