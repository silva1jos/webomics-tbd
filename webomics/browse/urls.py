from django.urls import path

from . import views

app_name = 'browse'
urlpatterns = [path('', views.IndexView.as_view(), name='index'),
               path('<int:pk>', views.detail, name='detail'),
               path('add', views.add, name='add'),
               path('add/submit', views.submit, name='submit')]
