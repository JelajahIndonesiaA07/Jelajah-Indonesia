from django.urls import path
from tempat_wisata.views import show_tempat_wisata
from tempat_wisata.views import add_tempat_wisata
from tempat_wisata.views import get_tempat_wisata
from tempat_wisata.views import delete_tempat_wisata
from tempat_wisata.views import show_tempat_wisata_json
from tempat_wisata.views import flutter_add_tempat_wisata
from tempat_wisata.views import flutter_delete_tempat_wisata

app_name = 'tempat_wisata'

urlpatterns = [
    path('', show_tempat_wisata, name='show_tempat_wisata'),
    path('add-tempat-wisata/', add_tempat_wisata, name='add_tempat_wisata'),
    path('get-tempat-wisata/', get_tempat_wisata, name='get_tempat_wisata'),
    path('delete-tempat-wisata/<int:id>', delete_tempat_wisata, name='delete_tempat_wisata'),
    path('get-tempat-wisata-flutter/', show_tempat_wisata_json, name="show_tempat_wisata_json"),
    path('add-tempat-wisata-flutter/', flutter_add_tempat_wisata, name="flutter_add_tempat_wisata"),
    path('delete-tempat-wisata-flutter/', flutter_delete_tempat_wisata, name="flutter_delete_tempat_wisata"),
]