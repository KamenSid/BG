from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, DeleteView, ListView, FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Replay
from BG.forms import DeleteReplayForm, CommentInputForm, SearchForm
from ..members.models import Guild


class IndexView(ListView):
    model = Replay
    template_name = 'testdb/index.html'
    context_object_name = 'test_replays'


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
                                                                                # History setup
        MAX_HISTORY = 10
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


class SearchView(FormView):
    template_name = 'testdb/search.html'
    form_class = SearchForm

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        game = self.request.GET.get('game')
        guild = self.request.GET.get('guild')

        search_results = Replay.objects.filter(title__icontains=query)

        if game:
            search_results = search_results.filter(game=game)

        if guild:
            search_results = search_results.filter(author__appuserprofile__guild_id=guild)
        return search_results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_results'] = self.get_queryset()
        return context
