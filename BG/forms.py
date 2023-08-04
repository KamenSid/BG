from django import forms
from BG.testdb.models import Replay
from BG.testdb.models import Comment
from BG.members.models import AppUserProfile, Guild


def get_choices(model, field):
    data = set(model.objects.values_list(field, flat=True).distinct())
    choices = [('', 'All')]
    choices.extend([[game_name, game_name] for game_name in data])
    return choices


class CreateReplay(forms.ModelForm):
    MAX_LENGTH_SMALL = 30
    MAX_LENGTH_LARGE = 300
    title = forms.CharField(label="", max_length=MAX_LENGTH_SMALL,
                            widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    game = forms.CharField(label="", max_length=MAX_LENGTH_SMALL,
                           widget=forms.TextInput(attrs={'placeholder': 'Game'}))
    description = forms.CharField(label="", max_length=MAX_LENGTH_LARGE,
                                  widget=forms.TextInput(attrs={'placeholder': 'Description'}))
    video_choice = forms.BooleanField(label="File Source", required=False, initial=False)
    video_url = forms.CharField(label="", max_length=MAX_LENGTH_LARGE,
                                required=False, widget=forms.TextInput(attrs={'placeholder': 'Video URL'}))
    video_upload = forms.FileField(
        label="", required=False, widget=forms.ClearableFileInput()
    )

    class Meta:
        model = Replay
        fields = ("title", "game", "description", "video_url", "video_upload")


class DeleteReplayForm(forms.ModelForm):
    class Meta:
        model = Replay
        fields = []


class LogInUser(forms.Form):
    username = forms.CharField(label="Username",
                               max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class CommentInputForm(forms.ModelForm):
    content = forms.CharField(label=False,
                              widget=forms.TextInput(attrs={"placeholder": "Your Comment"}))

    class Meta:
        model = Comment
        fields = ["content"]


class SearchForm(forms.Form):
    query = forms.CharField(label=False,
                            max_length=100,
                            required=False,
                            widget=forms.TextInput(attrs={"placeholder": "Search..."}))
    game = forms.ChoiceField(label='Game',
                             choices=[],
                             required=False)
    guild = forms.ModelChoiceField(queryset=Guild.objects.all(), required=False, empty_label="Select a Guild")

    search_members = forms.BooleanField(required=False, initial=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['game'].choices = get_choices(Replay, field="game")


class AppUserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUserProfile
        exclude = ['app_user', 'guild', 'steam_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['steam_id'].initial = instance.steam_id
