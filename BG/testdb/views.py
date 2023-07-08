from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Replay
from django.views.generic import DetailView, DeleteView, ListView
from BG.forms import DeleteReplayForm
from ..accounts.models import AppUser


class IndexView(ListView):
    model = Replay
    template_name = 'testdb/index.html'
    context_object_name = 'test_replays'


class ProfileView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = 'testdb/profile_view.html'
    context_object_name = 'appuser'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        uploaded_replays = Replay.objects.filter(author=user_id)
        liked_replays = Replay.objects.filter(likes__email=self.request.user.email)
        replays_count = uploaded_replays.count()
        context['test_replays'] = uploaded_replays
        context['replays_count'] = replays_count
        context['date_joined'] = self.request.user.last_login
        context['liked_replays'] = liked_replays
        return context


class ReplayDeleteView(LoginRequiredMixin, DeleteView):
    model = Replay
    template_name = "members/delete-replay.html"
    success_url = reverse_lazy("test_db_base")
    form_class = DeleteReplayForm


class ReplayDetailsView(DetailView):
    model = Replay
    template_name = "members/replay_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


def search_view(request):
    query = request.GET.get('search')
    if query is None:
        query = ""
    search_results = Replay.objects.filter(title__icontains=query)
    context = {
        'user': request.user,
        'search_results': search_results
    }
    return render(request, "testdb/search.html", context)
