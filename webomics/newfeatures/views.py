from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


from .forms import UploadFileForm, ExperimentFilterForm
from .filetools import handle_uploaded_file


def index_view(request):
    return render(request, 'newfeatures/index.html',
                  {'form': ExperimentFilterForm()})


def filter_exp(request):
    print('request recieved')
    form = ExperimentFilterForm(request.GET)
    print(form.filter())
    return render(request, 'newfeatures/load_experiment.html',
                  {'experiments': form.filter()})


class FileUploadView(generic.View):
    # Dont want to handle file uploads this way anymore
    form_class = UploadFileForm
    success_url = reverse_lazy('newfeatures:index')
    template_name = 'newfeatures/upload.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], request.POST['title'])
            return HttpResponseRedirect('/newfeatures')
        return render(request, 'newfeatures/upload.html', {'form': form})
