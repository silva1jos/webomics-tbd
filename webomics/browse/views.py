from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .forms import ExperimentForm, GeneColForm, GeneCountGroupsForm
from .models import Experiment
from .graphs import volcano_plot


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


class GraphView(generic.View):
    """ Base graph view for an experiment"""
    template_name = 'browse/graph.html'
    # success_url = reverse_lazy('browse:graph')

    def get(self, request, *args, **kwargs):
        exp = get_object_or_404(Experiment, pk=kwargs['pk'])
        form_gene = GeneColForm(count_file=exp.file_path.path)
        form_group = GeneCountGroupsForm(count_file=exp.file_path.path)
        return render(request, self.template_name,
                      {'form_gene': form_gene, 'form_group': form_group,
                       'experiment': exp})

    def post(self, request, *args, **kwargs):
        # Same for now
        exp = get_object_or_404(Experiment, pk=kwargs['pk'])
        form_gene = GeneColForm(count_file=exp.file_path.path)
        form_group = GeneCountGroupsForm(count_file=exp.file_path.path)
        return render(request, self.template_name,
                      {'form_gene': form_gene, 'form_group': form_group,
                       'experiment': exp})


def load_groups(request, pk):
    gene_col_idx = request.GET.get('gene_col_idx')
    exp = get_object_or_404(Experiment, pk=pk)
    form_group = GeneCountGroupsForm(gene_col_idx=gene_col_idx,
                                     count_file=exp.file_path.path)
    return render(request, 'browse/load_groups.html', {'form': form_group})


def load_volcano_plot(request, pk):
    exp = get_object_or_404(Experiment, pk=pk)
    data = dict(request.GET)
    gene_col = int(data.pop('Select Gene Column')[0])
    with open(exp.file_path.path) as f:
        gene_col = f.readline().rstrip().split('\t')[gene_col]

    data.pop('csrfmiddlewaretoken')
    group1 = []
    group2 = []
    for key, val in data.items():
        if val == ['True']:
            group2.append(key)
        elif val == ['False']:
            group1.append(key)
    plt_div = volcano_plot(exp.file_path.path, group1, group2, gene_col)
    return render(request, 'browse/load_graph.html', {'graph': plt_div})


def detail(request, pk):
    # Use generic ExpDetailView above
    experiment = get_object_or_404(Experiment, pk=pk)
    return render(request, 'browse/detail.html', {'experiment': experiment})
