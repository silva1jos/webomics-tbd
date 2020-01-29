from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from plotly.offline import plot
import plotly.graph_objs as go

from .forms import UploadFileForm
from .filetools import handle_uploaded_file


def graph_view(request):
    fig = go.Figure()
    scatter = go.Scatter(x=[0, 1, 2, 3], y=[0, 1, 2, 3],
                         mode='lines', name='test',
                         opacity=0.8, marker_color='green')
    fig.add_trace(scatter)  # might not want
    plt_div = plot(fig, output_type='div', include_plotlyjs=False,
                   config={'displaylogo': False})
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
