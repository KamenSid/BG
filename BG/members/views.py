from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from BG.testdb.models import Replay
from BG.forms import CreateReplay


def upload_replay(request):
    context = {
        "form": None,
        "message": "",
        "username": request.user.username
    }
    if request.method == "POST":
        form = CreateReplay(request.POST)
        if form.is_valid():
            replay = form.save(commit=False)
            replay.author = request.user
            replay.save()
            context["message"] = "You have uploaded a replay!"
            return redirect("index")
        else:
            context["message"] = "something went wrong, sorry"

    else:
        if not request.user.is_anonymous:
            context["message"] = "please upload a replay"
            context["form"] = CreateReplay()

            return render(request, template_name="members/upload_replay.html", context=context)

        return redirect("index")


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
