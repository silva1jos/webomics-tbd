from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'browse'
urlpatterns = [path('', views.IndexView.as_view(), name='index'),
               path('<int:pk>/delete', views.DelExpView.as_view(),
                    name='delete'),
               path('<int:pk>', views.ExpDetailView.as_view(), name='detail'),
               path('<int:pk>/graph', views.GraphView.as_view(), name='graph'),
               path('ajax/<int:pk>/load-groups/', views.load_groups,
                    name='ajax_load_groups'),
               path('ajax/<int:pk>/load_volcano_plot', views.load_volcano_plot,
                    name='ajax_load_volcano'),
               path('ajax/<int:pk>/load_pca', views.load_pca,
                    name='ajax_load_pca'),
               path('ajax/filter_exp', views.filter_exp,
                    name='ajax_filter_experiments'),
               path('add', views.AddView.as_view(), name='add')] + \
               static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Include the static code to be able to use load static to not provide files
