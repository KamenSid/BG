from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, TemplateView
from BG.testdb.models import Replay
from BG.members.models import AppUserProfile, Guild, Like
from BG.forms import CreateReplay, AppUserProfileForm, EditGuildForm
from BG.members.forms import GuildForm, GuildInviteForm
from steam import Steam

AppUser = get_user_model()

with open("steam_api.txt", "r") as file:
    STEAM_KEY = file.read().strip()


def get_profile(user):
    profile = get_object_or_404(AppUserProfile, app_user_id=user.id)
    return profile


@login_required
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


class UploadReplayView(LoginRequiredMixin, CreateView):
    model = Replay
    form_class = CreateReplay
    template_name = 'members/upload_replay.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = AppUserProfile
    form_class = AppUserProfileForm
    template_name = 'members/update_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(AppUserProfile, app_user_id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy("profile-details", kwargs={"pk": self.request.user.id})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())

        return render(request, self.template_name, {'form': form})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = AppUser
    template_name = 'members/profile_delete.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = AppUser.objects.get(pk=self.request.user.pk)
        user.appuserprofile.delete()
        return super().delete(request, *args, **kwargs)


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

            user_is_leader = self.object.leader == self.request.user
            context['user_is_leader'] = user_is_leader

        return context


class EditGuildView(LoginRequiredMixin, UpdateView):
    model = Guild
    template_name = 'members/guild_update.html'
    form_class = EditGuildForm
    success_url = reverse_lazy('guild-details')

    def get_object(self, queryset=None):
        guild_obj = self.request.user.guild.first()
        return guild_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = []

        return context


class GuildCreate(LoginRequiredMixin, CreateView):
    model = Guild
    form_class = GuildForm
    template_name = 'members/guild_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        chosen_leader = form.cleaned_data['leader']
        leader_profile = chosen_leader.appuserprofile
        leader_profile.guild = self.object
        leader_profile.save()

        self.object.members.add(chosen_leader)

        return response


def guild_add_members(request):
    guild_obj = request.user.guild.first()
    context = {}
    if request.method == 'POST':
        invite_form = GuildInviteForm(request.POST)
        if invite_form.is_valid():
            invited_username = invite_form.cleaned_data.get('invite_user')
            invited_user = AppUser.objects.filter(appuserprofile__username=invited_username).first()
            if invited_user:
                guild_obj.members.add(invited_user)
                context = {
                    "messages": f"You have added {invited_user.appuserprofile.username}"
                }
            else:
                context = {
                    "messages": "There is no such user!"
                }

            return redirect('guild-edit')
    else:
        invite_form = GuildInviteForm()

    context["invite_form"] = invite_form
    return render(request, template_name="members/guild_add_members.html", context=context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = 'members/profile_view.html'
    context_object_name = 'appuser'

    def get_context_data(self, **kwargs):

        own_profile = False
        steam = Steam(STEAM_KEY)
        player_info = ""
        profile_user = self.get_object()
        if self.request.user == profile_user:
            own_profile = True

        if profile_user.appuserprofile.steam_id:
            user_steam_id = profile_user.appuserprofile.steam_id
            cached_player_info = cache.get(f'player_info_{user_steam_id}')
            cached_player_recent_games = cache.get(f'player_recent_games_{user_steam_id}')

            if not cached_player_info or not cached_player_recent_games:
                player_info = steam.users.get_user_details(user_steam_id)['player']
                player_recent_games = steam.users.get_user_recently_played_games(user_steam_id)['games']
                cache.set(f'player_info_{user_steam_id}', player_info, 36000)
                cache.set(f'player_recent_games_{user_steam_id}', player_recent_games, 36000)
            else:
                player_info = cached_player_info
                player_recent_games = cached_player_recent_games

        uploaded_replays = Replay.objects.filter(author=profile_user.pk)
        liked_replays = Replay.objects.filter(like__user=profile_user.pk)
        replays_count = uploaded_replays.count()

        context = super().get_context_data(**kwargs)
        context['test_replays'] = uploaded_replays
        context['replays_count'] = replays_count
        context['liked_replays'] = liked_replays
        context['owner'] = own_profile

        if player_info:
            context['player_info'] = player_info
            context['player_avatar'] = player_info['avatarfull']
            context['player_recent_games'] = player_recent_games

        return context
