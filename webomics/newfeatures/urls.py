from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'newfeatures'
urlpatterns = [path('', views.index_view, name='index'),
               path('ajax/filter_exp', views.filter_exp,
                    name='ajax_filter_experiments')] + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# path('upload', views.FileUploadView.as_view(), name='upload')]
