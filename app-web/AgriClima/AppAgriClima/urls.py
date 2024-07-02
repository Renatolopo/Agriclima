from django.urls import path
from .views import index, get_estacoes, download_station_data_view, serve_csv, csv_view, download_multiple_stations_data
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='index'),
    path('get_estacoes/', get_estacoes, name='get_estacoes'),
    path('download/', download_station_data_view, name='download_station_data'),
    path('data/saida/<str:filename>', serve_csv, name='serve_csv'),
    path('csv/<str:file_name>/<path:file_path>/', csv_view, name='csv_view'),
    path('download-multiple-stations/', download_multiple_stations_data, name='download_multiple_stations_data'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)