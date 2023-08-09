from django.db.models import Count
from django.views.generic import ListView, FormView

from .models import Replay
from BG.forms import SearchForm


class IndexView(ListView):
    model = Replay
    template_name = 'testdb/index.html'
    context_object_name = 'test_replays'

    def get_queryset(self):
        replays = Replay.objects.annotate(like_count=Count('like')).order_by('-like_count', 'title')

        return replays


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
