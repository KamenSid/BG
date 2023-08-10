from django.shortcuts import render
from django.views.generic import ListView, FormView

from .models import Replay
from BG.forms import SearchForm
from BG.members.views import InfoMixin


class IndexView(ListView, InfoMixin):
    model = Replay
    template_name = 'testdb/index.html'
    context_object_name = 'test_replays'

    def get_queryset(self):
        replays = self.replays_ranking()
        return replays

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guild_ranking'] = self.guilds_ranking()[:5]
        context['replays_ranking'] = self.replays_ranking()[:5]
        return context


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


def error_404(request, data):
    return render(request, '404.html', data)


def error_500(request):
    return render(request, '500.html')
