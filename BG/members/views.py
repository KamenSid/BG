from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from BG.testdb.models import Replay
from BG.members.models import AppUserProfile, Guild, Like
from BG.forms import CreateReplay, AppUserProfileForm, EditGuildForm
from steam import Steam

AppUser = get_user_model()

with open("steam_api.txt", "r") as file:
    STEAM_KEY = file.read().strip()


def get_profile(user):
    profile = get_object_or_404(AppUserProfile, app_user_id=user.id)
    return profile


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


@login_required
def like_replay(request, replay_pk):
    replay = get_object_or_404(Replay, pk=replay_pk)
    user = request.user
    if Like.objects.filter(user=user, replay=replay).exists():
        Like.objects.filter(user=user, replay=replay).delete()
    else:
        Like.objects.create(user=user, replay=replay)
    return redirect('replay-details', pk=replay_pk)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = AppUserProfile
    form_class = AppUserProfileForm
    template_name = 'members/update_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(AppUserProfile, app_user_id=self.request.user.id)

    def get_success_url(self):
        profile = get_object_or_404(AppUserProfile, app_user_id=self.request.user.id)
        return reverse_lazy("profile-details", kwargs={"pk": profile.pk})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())

        return render(request, self.template_name, {'form': form})


class GuildDetailsView(LoginRequiredMixin, DetailView):
    model = Guild
    template_name = 'members/guild_details.html'

    def get_object(self, queryset=None):
        guild = self.request.user.appuserprofile.guild
        return guild

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            members = self.object.members.all()
            replays_by_guild_members = Replay.objects.filter(author__in=members)
            total_guild_likes = 0
            for replay in replays_by_guild_members:
                total_guild_likes += replay.like_set.count()
            context['replays_by_members'] = replays_by_guild_members
            context['total_guild_likes'] = total_guild_likes
            context['members'] = members
        return context


class EditGuildView(LoginRequiredMixin, UpdateView):
    model = Guild
    template_name = 'members/guild_update.html'
    form_class = EditGuildForm
    success_url = reverse_lazy('guild-details')

    def get_object(self, queryset=None):
        guild = self.request.user.guild.first()
        return guild


class ProfileView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = 'members/profile_view.html'
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
        liked_replays = Replay.objects.filter(like__user=user_id)
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
