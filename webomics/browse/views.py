from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import ExperimentForm
from .models import Experiment


class IndexView(generic.ListView):
    template_name = 'browse/index.html'
    context_object_name = 'latest_experiments'

    def get_queryset(self):
        """ Return the last five published experiments."""
        return Experiment.objects.filter(last_update__lte=timezone.now()) \
                         .order_by('-date_pref')[:5]


class AddView(generic.View):
    template_name = 'browse/add.html'
    form_class = ExperimentForm
    success_url = reverse_lazy('browse:index')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('browse:index'))
        else:
            print('invalid')
            print(form.errors)
        return render(request, self.template_name, {'form': form})


class DelExpView(generic.DeleteView):
    template_name = 'browse/delete.html'
    model = Experiment
    # Need reverse lazy to prevent a circular import error
    success_url = reverse_lazy('browse:index')


class ExpDetailView(generic.DetailView):
    model = Experiment
    template_name = 'browse/detail.html'


def detail(request, pk):
    # Use generic ExpDetailView above
    experiment = get_object_or_404(Experiment, pk=pk)
    return render(request, 'browse/detail.html', {'experiment': experiment})
