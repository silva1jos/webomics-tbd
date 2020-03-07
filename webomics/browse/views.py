from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import ExperimentForm, GeneColForm, GeneCountGroupsForm, \
    ExperimentFilterForm, SampleGroupsForm
from .models import Experiment, ExperimentCalc
from . import graphs, expcalcs


class IndexView(generic.FormView):
    template_name = 'browse/index.html'
    form_class = ExperimentFilterForm
    success_url = reverse_lazy('browse:index')


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


def filter_exp(request):
    print('request recieved')
    form = ExperimentFilterForm(request.GET)
    return render(request, 'browse/load_experiment.html',
                  {'experiments': form.filter()})


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
        form_pca = SampleGroupsForm(count_file=exp.file_path.path)
        return render(request, self.template_name,
                      {'form_gene': form_gene, 'form_group': form_group,
                       'experiment': exp, 'form_pca': form_pca})

    def post(self, request, *args, **kwargs):
        # Same for now
        exp = get_object_or_404(Experiment, pk=kwargs['pk'])
        form_gene = GeneColForm(count_file=exp.file_path.path)
        form_group = GeneCountGroupsForm(count_file=exp.file_path.path)
        form_pca = SampleGroupsForm(count_file=exp.file_path.path)
        return render(request, self.template_name,
                      {'form_gene': form_gene, 'form_group': form_group,
                       'experiment': exp, 'form_pca': form_pca})


def load_groups(request, pk):
    gene_col_idx = request.GET.get('gene_col_idx')
    exp = get_object_or_404(Experiment, pk=pk)
    form_group = GeneCountGroupsForm(gene_col_idx=gene_col_idx,
                                     count_file=exp.file_path.path)
    form_pca = SampleGroupsForm(gene_col_idx=gene_col_idx,
                                count_file=exp.file_path.path)
    return JsonResponse({'groups': form_group.as_table(),
                         'pca': form_pca.as_table()})


def load_volcano_plot(request, pk):
    exp = get_object_or_404(Experiment, pk=pk)
    data = dict(request.GET)
    gene_col = int(data.pop('Select Gene Column')[0])
    with open(exp.file_path.path) as f:
        gene_col = f.readline().rstrip().split('\t')[gene_col]
    group_a = []
    group_b = []
    for key, val in data.items():
        if val == ['True']:
            group_b.append(key)
        elif val == ['False']:
            group_a.append(key)
    q = ExperimentCalc.objects.filter(exp_ref__id=exp.id, calc_name='volcano')
    for sample in group_a:
        q = q.filter(calcoptions__value__exact=sample,
                     calcoptions__name__exact='group_a')
    for sample in group_b:
        q = q.filter(calcoptions__value__exact=sample,
                     calcoptions__name__exact='group_b')
    print(q)
    if not q.exists():
        print('making calc')
        # Make a list to use the same slicing as a queryset
        q = [expcalcs.volcano_calc(exp, group_a, group_b, gene_col)]
    plt_div = graphs.volcano_plot(q[0])
    return render(request, 'browse/load_graph.html', {'graph': plt_div})


def load_pca(request, pk):
    exp = get_object_or_404(Experiment, pk=pk)
    data = dict(request.GET)
    print(data)
    gene_col = int(data.pop('gene_col')[0])
    with open(exp.file_path.path) as f:
        samples = f.readline().rstrip().split('\t')
    del samples[gene_col]
    groups = []
    for s in samples:
        groups.append(data.get(s, "None")[0])
    plt_div = graphs.pca_plot(exp.file_path.path, groups=groups,
                              index_col=gene_col)
    return render(request, 'browse/load_graph.html', {'graph': plt_div})


def detail(request, pk):
    # Use generic ExpDetailView above
    experiment = get_object_or_404(Experiment, pk=pk)
    return render(request, 'browse/detail.html', {'experiment': experiment})
