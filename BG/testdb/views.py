from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Replay
from django.views.generic import DetailView, DeleteView
from BG.forms import DeleteReplayForm


def index(request):
    test_replays = Replay.objects.all()

    context = {"test_replays": test_replays,
               "username": "Unknown",
               "date": "you haven't joined yet"}

    if not request.user.is_anonymous:
        username = request.user.username
        user_id = request.user.id

        context["username"] = username
        context["user_id"] = user_id

        return render(request, 'testdb/index.html', context)

    return render(request, "testdb/index.html", context)


def test_view(request):
    user_id = request.user.id
    test_replays = Replay.objects.filter(author=user_id)
    liked_replays = Replay.objects.filter(likes__username=request.user.username)
    replays_count = len(test_replays)
    context = {
        "user_id": user_id,
        "username": request.user.username,
        "test_replays": test_replays,
        "replays_count": replays_count,
        "date_joined": request.user.date_joined,
        "liked_replays": liked_replays,
    }
    return render(request, 'testdb/test_view.html', context)


class ReplayDeleteView(DeleteView):
    model = Replay
    template_name = "testdb/delete-replay.html"
    success_url = reverse_lazy("test_db_base")
    form_class = DeleteReplayForm


class ReplayDetailsView(DetailView):
    model = Replay

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
