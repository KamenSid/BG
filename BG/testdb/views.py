from django.shortcuts import render, redirect
from .models import Replay


def index(request):
    context = {"replays": []}
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
    liked_replays = Replay.objects.filter(like__owner=user_id)
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


def delete_replay(request, pk):
    test_replay = Replay.objects.all().filter(pk=pk)
    test_replay.delete()
    return redirect("index")
