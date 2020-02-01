from django.urls import path

from . import views

app_name = 'browse'
urlpatterns = [path('', views.IndexView.as_view(), name='index'),
               path('<int:pk>/delete', views.DelExpView.as_view(),
                    name='delete'),
               path('<int:pk>', views.ExpDetailView.as_view(), name='detail'),
               path('add', views.AddView.as_view(), name='add')]
