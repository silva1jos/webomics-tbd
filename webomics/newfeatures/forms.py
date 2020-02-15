from django import forms

from browse.models import Experiment


class ExperimentFilterForm(forms.Form):
    """ Form for filtering Experiments """
    name = forms.CharField(required=False)
    perf_low = forms.DateField(required=False, widget=forms.SelectDateWidget())
    perf_high = forms.DateField(required=False,
                                widget=forms.SelectDateWidget())
    upd_low = forms.DateField(required=False, widget=forms.SelectDateWidget())
    upd_high = forms.DateField(required=False, widget=forms.SelectDateWidget())
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
                q = q.filter(date_perf__gte=self.cleaned_data['perf_low'])
            if self.cleaned_data['perf_high'] is not None:
                q = q.filter(date_perf__lte=self.cleaned_data['perf_high'])
            if self.cleaned_data['upd_low'] is not None:
                q = q.filter(last_update__gte=self.cleaned_data['upd_low'])
            if self.cleaned_data['upd_high'] is not None:
                q = q.filter(last_update__lte=self.cleaned_data['upd_high'])
            return q


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
