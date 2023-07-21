from django import forms
from BG.testdb.models import Replay
from BG.testdb.models import Comment
from BG.members.models import AppUserProfile, Guild


class CreateReplay(forms.ModelForm):
    title = forms.CharField(label="title", max_length=30)
    game = forms.CharField(label="game", max_length=30)
    description = forms.CharField(label="description", max_length=300)
    video_url = forms.CharField(label="video", max_length=200, required=False)
    video_upload = forms.FileField(required=False)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['game'].choices = self.get_choices(Replay, field="game")

    @staticmethod
    def get_choices(model, field):
        games = set(model.objects.values_list(field, flat=True).distinct())
        choices = [('', 'All')]
        choices.extend([[game_name, game_name] for game_name in games])
        return choices


class AppUserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUserProfile
        exclude = ['app_user', 'guild', 'steam_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['steam_id'].initial = instance.steam_id


class EditGuildForm(forms.ModelForm):
    class Meta:
        model = Guild
        fields = '__all__'
