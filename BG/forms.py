from django import forms
from BG.testdb.models import Replay
from BG.testdb.models import Comment
from BG.members.models import AppUserProfile


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['game'].choices = self.get_category_choices()

    def get_category_choices(self):
        games = set(Replay.objects.values_list('game', flat=True).distinct())
        choices = [('', 'All')]
        choices.extend([[game_name, game_name] for game_name in games])
        return choices


class AppUserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUserProfile
        fields = "__all__"
