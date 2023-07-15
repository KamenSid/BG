from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from BG.testdb.models import Replay
from BG.forms import CreateReplay


class UploadReplayView(LoginRequiredMixin, CreateView):
    model = Replay
    form_class = CreateReplay
    template_name = 'members/upload_replay.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def update_replay(request, replay_pk):
    replay = get_object_or_404(Replay, pk=replay_pk)
    form = CreateReplay(request.POST or None, instance=replay)

    if form.is_valid():
        form.save()
        return redirect("index")
    context = {
        "replay_name": replay.title,
        "form": form
    }
    return render(request, template_name="members/update_replay.html", context=context)


def like_replay(request, replay_pk):
    replay = get_object_or_404(Replay, pk=replay_pk)
    user = request.user

    replay.likes.add(user)

    replay.save()
    return redirect(request.META['HTTP_REFERER'])