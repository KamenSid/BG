from django import forms
from BG.testdb.models import Replay
from BG.testdb.models import Comment


class CreateReplay(forms.ModelForm):
    title = forms.CharField(label="title", max_length=30)
    game = forms.CharField(label="game", max_length=30)
    description = forms.CharField(label="description", max_length=300)
    video = forms.CharField(label="video", max_length=200)

    class Meta:
        model = Replay
        fields = ("title", "game", "description", "video")


class DeleteReplayForm(forms.ModelForm):
    class Meta:
        model = Replay
        fields = []


class LogInUser(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class CommentInputForm(forms.ModelForm):
    content = forms.CharField(label=False, widget=forms.TextInput(attrs={"placeholder": "Your Comment"}))

    class Meta:
        model = Comment
        fields = ["content"]
