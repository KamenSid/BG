from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, DeleteView, ListView, FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Replay
from BG.forms import DeleteReplayForm, CommentInputForm, SearchForm
from ..accounts.models import AppUser
from steam import Steam

with open("steam_api.txt", "r") as file:
    STEAM_KEY = file.read().strip()


class IndexView(ListView):
    model = Replay
    template_name = 'testdb/index.html'
    context_object_name = 'test_replays'


class ProfileView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = 'testdb/profile_view.html'
    context_object_name = 'appuser'

    def get_context_data(self, **kwargs):
        steam = Steam(STEAM_KEY)
        player_info = ""
        if self.request.user.appuserprofile.steam_id:
            user_steam_id = self.request.user.appuserprofile.steam_id
            player_info = steam.users.get_user_details(user_steam_id)['player']
            player_recent_games = steam.users.get_user_recently_played_games(user_steam_id)['games']

        user_id = self.request.user.id
        uploaded_replays = Replay.objects.filter(author=user_id)
        liked_replays = Replay.objects.filter(likes__email=self.request.user.email)
        replays_count = uploaded_replays.count()

        context = super().get_context_data(**kwargs)
        context['test_replays'] = uploaded_replays
        context['replays_count'] = replays_count
        context['date_joined'] = self.request.user.last_login
        context['liked_replays'] = liked_replays
        if player_info:
            context['player_info'] = player_info
            context['player_avatar'] = player_info['avatarfull']
            context['player_recent_games'] = player_recent_games

        return context


class ReplayDeleteView(LoginRequiredMixin, DeleteView):
    model = Replay
    template_name = "members/delete_replay.html"
    form_class = DeleteReplayForm

    def get_success_url(self):
        return reverse_lazy("profile-details", kwargs={"pk": self.request.user.pk})


class ReplayDetailsView(DetailView):
    model = Replay
    template_name = "members/replay_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentInputForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentInputForm(request.POST)
        self.object = self.get_object()

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.replay = self.object
            new_comment.save()
            return redirect('replay-details', pk=self.object.pk)
        else:
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)


class SearchView(FormView):
    template_name = 'testdb/search.html'
    form_class = SearchForm

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        game = self.request.GET.get('game')

        search_results = Replay.objects.filter(title__icontains=query)

        if game:
            search_results = search_results.filter(game=game)

        return search_results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_results'] = self.get_queryset()
        return context

# def search_view(request):
#     query = request.GET.get('search')
#     if query is None:
#         query = ""
#     search_results = Replay.objects.filter(title__icontains=query)
#     context = {
#         'user': request.user,
#         'search_results': search_results
#     }
#     return render(request, "testdb/search.html", context)
