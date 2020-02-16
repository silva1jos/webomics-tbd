from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'pipelines'
urlpatterns = [path('', views.index_view, name='index')] + \
               static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
