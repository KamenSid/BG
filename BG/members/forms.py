from django import forms
from django.contrib.auth import get_user_model
from .models import Guild

User = get_user_model()


class GuildForm(forms.ModelForm):
    MAX_LENGTH = 50
    MAX_LENGTH_URL = 300

    name = forms.CharField(label="", max_length=MAX_LENGTH,
                           widget=forms.TextInput(attrs={'placeholder': 'Guild Name'}))
    banner = forms.URLField(label="", max_length=MAX_LENGTH_URL,
                            required=False, widget=forms.TextInput(attrs={'placeholder': 'Guild Banner URL'}))

    class Meta:
        model = Guild
        fields = ['name', 'leader', 'banner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leader'].queryset = User.objects.filter(appuserprofile__guild=None)


class EditGuildForm(forms.ModelForm):
    MAX_LENGTH = 50
    MAX_LENGTH_URL = 300

    name = forms.CharField(label="", max_length=MAX_LENGTH,
                           widget=forms.TextInput(attrs={'placeholder': 'Guild Name'}))

    banner = forms.URLField(label="", max_length=MAX_LENGTH_URL,
                            required=False, widget=forms.TextInput(attrs={'placeholder': 'Guild Banner'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        guild_instance = kwargs['instance']
        self.fields['leader'].queryset = guild_instance.members.all()

    class Meta:
        model = Guild
        fields = ('name', 'leader', 'banner')


class GuildInviteForm(forms.Form):
    invite_user = forms.CharField(label="", max_length=100,
                                  widget=forms.TextInput(attrs={"placeholder": "User to add or remove"}))
