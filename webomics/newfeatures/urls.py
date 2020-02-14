from django.urls import path

from . import views

app_name = 'newfeatures'
urlpatterns = [path('', views.graph_view, name='index'),
               path('upload', views.FileUploadView.as_view(), name='upload')]
