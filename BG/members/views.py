import asyncio
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions
from .serializers import ReplaySerializer
from BG.testdb.models import Replay
from BG.members.models import AppUserProfile, Guild, Like
from BG.forms import CreateReplay, AppUserProfileForm, CommentInputForm, DeleteReplayForm
from BG.members.forms import GuildForm, GuildInviteForm, EditGuildForm, GuildRemoveForm
from steam import Steam

AppUser = get_user_model()

with open("steam_api.txt", "r") as file:
    STEAM_KEY = file.read().strip()


@login_required
def like_replay(request, replay_pk):
    replay = get_object_or_404(Replay, pk=replay_pk)
    user = request.user
    if Like.objects.filter(user=user, replay=replay).exists():
        Like.objects.filter(user=user, replay=replay).delete()
    else:
        Like.objects.create(user=user, replay=replay)
    return redirect('replay-details', pk=replay_pk)


@login_required
def guild_add_members(request):
    guild_obj = request.user.appuserprofile.guild  # Getting the users guild
    context = {
        "guild_name": guild_obj.name
    }
    if request.method == 'POST':
        invite_form = GuildInviteForm(request.POST)
        remove_form = GuildRemoveForm(request.POST, guild=guild_obj)

        if invite_form.is_valid():  # Inviting members to a guild
            invited_username = invite_form.cleaned_data.get('invite_member')
            try:
                invited_user = AppUser.objects.get(appuserprofile__username=invited_username)

                if invited_user.appuserprofile.guild is None:  # Checking if the user is a member of a guild
                    guild_obj.members.add(invited_user)
                    invited_user.appuserprofile.guild = guild_obj
                    invited_user.appuserprofile.save()
                    context["messages"] = [f"You have added {invited_username} to {guild_obj.name}"]
                else:
                    context["messages"] = [f"The user: {invited_username} is already member of a guild."]
            except AppUser.DoesNotExist:
                context["messages"] = [f"User with the name {invited_username} does not exist!"]
                context["invite_form"] = GuildInviteForm()

        elif remove_form.is_valid():  # Removing members from the guild
            removed_user_name = remove_form.cleaned_data.get('remove_member')
            removed_user = AppUser.objects.get(appuserprofile__username=removed_user_name)
            if removed_user in guild_obj.members.all():
                guild_obj.members.remove(removed_user)
                removed_user.appuserprofile.guild = None
                removed_user.appuserprofile.save()
                context["messages"] = [f"You have removed {removed_user.appuserprofile.username}"]
                return redirect('guild-details', pk=guild_obj.pk)
    else:
        invite_form = GuildInviteForm()
        remove_form = GuildRemoveForm(None, guild=guild_obj)
        # Passing the guild to the remove form, so it can show only members to remove.
    context["invite_form"] = invite_form
    context['remove_form'] = remove_form
    return render(request, 'members/guild_add_members.html', context)


class UploadReplayView(LoginRequiredMixin, CreateView):
    model = Replay
    form_class = CreateReplay
    template_name = 'members/replay_upload.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Setting the author as the user uploading the replay
        return super().form_valid(form)


class ReplayDeleteView(LoginRequiredMixin, DeleteView):
    model = Replay
    template_name = "members/replay_delete.html"
    form_class = DeleteReplayForm

    def get_success_url(self):
        return reverse_lazy("profile-details", kwargs={"pk": self.request.user.pk})

    def dispatch(self, request, *args, **kwargs):
        replay = self.get_object()
        if replay.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ReplayDetailsView(DetailView):
    model = Replay
    template_name = "members/replay_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # History setup
        MAX_HISTORY = 5
        history = self.request.session.get('history', [])
        replay_info = {'title': self.object.title,
                       'pk': self.object.pk
                       }
        if replay_info in history:
            history.remove(replay_info)
        history.insert(0, replay_info)
        self.request.session['history'] = history[:MAX_HISTORY]

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


class UpdateReplayView(LoginRequiredMixin, UpdateView):
    model = Replay
    form_class = CreateReplay
    template_name = "members/replay_update.html"
    success_url = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        replay = self.get_object()
        if replay.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = 'members/profile_view.html'
    context_object_name = 'appuser'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        steam = Steam(STEAM_KEY)

        profile_user = self.get_object()
        uploaded_replays = Replay.objects.filter(author=profile_user.pk)
        liked_replays = Replay.objects.filter(like__user=profile_user.pk)
        replays_count = uploaded_replays.count()
        own_profile = self.request.user == profile_user  # Checking if the logged user is the owner of the profile

        async def get_steam_info(steam_id):
            try:
                pd = steam.users.get_user_details(steam_id)['player']
                pg = steam.users.get_user_recently_played_games(steam_id)['games']
                return pd, pg
            except Exception as e:
                context["messages"] = f"An error occurred while fetching Steam information: {e}"

        if profile_user.appuserprofile.steam_id:
            user_steam_id = profile_user.appuserprofile.steam_id
            try:
                player_info, player_recent_games = asyncio.run(
                    get_steam_info(user_steam_id))  # Using asyncio to run the function
                cache.set(f'player_info_{user_steam_id}', player_info, 36000)
                cache.set(f'player_recent_games_{user_steam_id}', player_recent_games, 36000)
                context['player_info'] = player_info
                context['player_avatar'] = player_info['avatarfull']
                context['player_recent_games'] = player_recent_games
            except Exception as ve:
                context["messages"] = [f"There is an error {ve}"]
        else:
            context["messages"] = [f"{profile_user.appuserprofile.username} didnt add a Steam ID."]

        context['test_replays'] = uploaded_replays
        context['replays_count'] = replays_count
        context['liked_replays'] = liked_replays
        context['owner'] = own_profile

        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = AppUserProfile
    form_class = AppUserProfileForm
    template_name = 'members/profile_update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(AppUserProfile, app_user_id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy("profile-details", kwargs={"pk": self.request.user.id})

    def post(self, request, *args, **kwargs):  # Saving the form with the picture file if there is one.
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            members = self.object.members.all()
            replays_by_guild_members = Replay.objects.filter(author__in=members)
            total_guild_likes = 0
            for replay in replays_by_guild_members:
                total_guild_likes += replay.like_set.count()
            user_is_leader = self.object.leader == self.request.user
            context['replays_by_members'] = replays_by_guild_members
            context['total_guild_likes'] = total_guild_likes
            context['members'] = members
            context['user_is_leader'] = user_is_leader

        return context


class EditGuildView(LoginRequiredMixin, UpdateView):
    model = Guild
    template_name = 'members/guild_update.html'
    form_class = EditGuildForm

    def get_object(self, queryset=None):
        guild_obj = self.request.user.guild.first()
        if self.request.user == guild_obj.leader:
            return guild_obj
        else:
            raise PermissionDenied

    def form_valid(self, form):
        guild = self.object
        # Managing the staff status of the old and the new leader, since only guild leaders have staff status.
        old_leader = guild.leader
        new_leader = form.cleaned_data['leader']
        if new_leader != old_leader:
            old_leader.is_staff = False
            old_leader.save()
            new_leader.is_staff = True
            new_leader.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = []
        return context

    def get_success_url(self):
        guild_pk = self.object.pk
        success_url = reverse_lazy('guild-details', kwargs={'pk': guild_pk})
        return success_url


class GuildCreate(LoginRequiredMixin, CreateView):
    model = Guild
    form_class = GuildForm
    template_name = 'members/guild_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        chosen_leader = form.cleaned_data['leader']

        chosen_leader.is_staff = True
        chosen_leader.save()
        leader_profile = chosen_leader.appuserprofile
        leader_profile.guild = self.object
        leader_profile.save()

        self.object.members.add(chosen_leader)

        return response


# REST API Views


class ReplayListAPIView(generics.ListAPIView, LoginRequiredMixin):
    queryset = Replay.objects.all()
    serializer_class = ReplaySerializer


def replay_list_frontend_view(request):
    return render(request, 'testdb/API_list.html')


class ReplayDetailAPIView(generics.RetrieveUpdateDestroyAPIView, LoginRequiredMixin, DjangoModelPermissions):
    queryset = Replay.objects.all()
    serializer_class = ReplaySerializer
