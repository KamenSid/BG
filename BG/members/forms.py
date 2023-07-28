from django import forms
from django.contrib.auth import get_user_model
from .models import Guild

User = get_user_model()


class GuildForm(forms.ModelForm):
    class Meta:
        model = Guild
        fields = ['name', 'leader', 'banner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leader'].queryset = User.objects.filter(appuserprofile__guild=None)


class GuildInviteForm(forms.Form):
    invite_user = forms.CharField(label="Invite User", max_length=100)
