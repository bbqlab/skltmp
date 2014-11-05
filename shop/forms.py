from django import forms
from django.core.exceptions import ValidationError


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