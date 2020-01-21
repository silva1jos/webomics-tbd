from datetime import datetime

from django import forms

from .models import Experiment


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class ExperimentForm(forms.ModelForm):
    date_performed = forms.DateField(widget=forms.SelectDateWidget())
    time_performed = forms.TimeField(widget=TimeInput())

    class Meta:
        model = Experiment
        fields = ['exp_name', 'date_performed', 'time_performed', 'file_type',
                  'file_name', 'author', 'version', 'comments']

    def save(self, commit=True):
        model = super(ExperimentForm, self).save(commit=False)
        model.date_pref = datetime.combine(self.cleaned_data['date_performed'],
                                           self.cleaned_data['time_performed'])
        if commit:
            model.save()
        return model
