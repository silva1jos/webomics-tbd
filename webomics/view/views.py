import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .graphs import volcano_plot
from .forms import UploadFileForm
from .filetools import handle_uploaded_file


def graph_view(request):
    plt_div = volcano_plot(os.path.join(os.path.dirname(__file__),
                                        'files/test4.csv'),
                           ['SRX014818and9', 'SRX014820and1', 'SRX014822and3'],
                           ['SRX014824and5', 'SRX014826and7', 'SRX014828and9'],
                           'gene')
    return render(request, 'view/index.html', {'graph': plt_div})


class FileUploadView(generic.View):
    form_class = UploadFileForm
    success_url = reverse_lazy('view:index')
    template_name = 'view/upload.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], request.POST['title'])
            return HttpResponseRedirect('/view')
        return render(request, 'view/upload.html', {'form': form})
