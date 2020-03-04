from datetime import datetime

from django import forms
from django.utils import timezone

from .models import Experiment


class TimeInput(forms.TimeInput):
    input_type = 'time'


class ExperimentForm(forms.ModelForm):
    date_performed = forms.DateField(widget=forms.SelectDateWidget(
        years=range(2000, timezone.now().year + 1)
    ))
    time_performed = forms.TimeField(widget=TimeInput())
    file = forms.FileField()

    class Meta:
        model = Experiment
        fields = ['exp_name', 'date_performed', 'time_performed', 'file_type',
                  'file_name', 'author', 'version', 'comments']

    def save(self, commit=True):
        model = super(ExperimentForm, self).save(commit=False)
        model.file_path = self.cleaned_data['file']
        model.date_pref = datetime.combine(self.cleaned_data['date_performed'],
                                           self.cleaned_data['time_performed'])
        if commit:
            model.save()
        return model


class ExperimentFilterForm(forms.Form):
    """ Form for filtering Experiments """
    dateWidget = forms.SelectDateWidget(
        years=range(2000, timezone.now().year + 1))
    name = forms.CharField(required=False)
    perf_low = forms.DateField(required=False, widget=dateWidget)
    perf_high = forms.DateField(required=False, widget=dateWidget)
    upd_low = forms.DateField(required=False, widget=dateWidget)
    upd_high = forms.DateField(required=False, widget=dateWidget)
    author = forms.CharField(required=False)
    ver_gte = forms.IntegerField(initial=0, required=False)

    def __init__(self, *args, **kwargs):
        super(ExperimentFilterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-filter'

    def filter(self):
        """ Given the form fields fitlers experiments, returning the resulting
            query set."""
        if self.is_valid():
            q = Experiment.objects.filter(
                exp_name__icontains=self.cleaned_data['name'],
                author__icontains=self.cleaned_data['author'],
                version__gte=self.cleaned_data['ver_gte'],)
            if self.cleaned_data['perf_low'] is not None:
                q = q.filter(date_pref__gte=self.cleaned_data['perf_low'])
            if self.cleaned_data['perf_high'] is not None:
                q = q.filter(date_pref__lte=self.cleaned_data['perf_high'])
            if self.cleaned_data['upd_low'] is not None:
                q = q.filter(last_update__gte=self.cleaned_data['upd_low'])
            if self.cleaned_data['upd_high'] is not None:
                q = q.filter(last_update__lte=self.cleaned_data['upd_high'])
            return q


class GeneCountForm(forms.Form):
    """ Empty Gene Count Form """
    def __init__(self, *args, gene_col_idx=0, **kwargs):
        count_file = kwargs.pop('count_file')
        super(forms.Form, self).__init__(*args, **kwargs)
        with open(count_file) as f:
            self.columns = f.readline().rstrip().split('\t')
        try:
            self.gene_col_idx = int(gene_col_idx)
        except ValueError:
            raise ValueError('GeneCountForm cannot update with %s'
                             % gene_col_idx)


class GeneColForm(GeneCountForm):
    def __init__(self, *args, **kwargs):
        # Sets columns and gene_col_index
        super(GeneColForm, self).__init__(*args, **kwargs)
        col_choices = []
        for i in range(len(self.columns)):
            col_choices.append((i, self.columns[i]))
        self.fields['Select Gene Column'] = forms.ChoiceField(
            choices=col_choices,
            initial=self.gene_col_idx,
            # Needs to be post-text for some reason?
            widget=forms.Select(attrs={'id': 'gene-selector'}))


class GeneCountGroupsForm(GeneCountForm):
    group_choices = ((False, "Group 1"), (True, "Group 2"),)

    def __init__(self, *args, **kwargs):
        super(GeneCountGroupsForm, self).__init__(*args, **kwargs)
        copy = list(self.columns)   # Might make tables update in future
        del copy[self.gene_col_idx]
        for col in copy:
            self.fields[col] = forms.ChoiceField(choices=self.group_choices,
                                                 initial=False)


class SampleGroupsForm(GeneCountForm):
    def __init__(self, *args, **kwargs):
        super(SampleGroupsForm, self).__init__(*args, **kwargs)
        copy = list(self.columns)
        del copy[self.gene_col_idx]
        for col in copy:
            self.fields[col] = forms.CharField(max_length=200)
