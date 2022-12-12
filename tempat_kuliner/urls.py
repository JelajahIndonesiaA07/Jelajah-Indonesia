from django.urls import path
from tempat_kuliner.views import show_tempat_kuliner
from tempat_kuliner.views import add_tempat_kuliner
from tempat_kuliner.views import get_tempat_kuliner
from tempat_kuliner.views import delete_tempat_kuliner
# from tempat_kuliner.views import AddKuliner_flutter
from tempat_kuliner.views import show_tempat_kuliner_json
from tempat_kuliner.views import add_data
from tempat_kuliner.views import delete_data
from tempat_kuliner.views import get_tempat_kuliner_by_user_id

app_name = 'tempat_kuliner'

urlpatterns = [
    path('', show_tempat_kuliner, name='show_tempat_kuliner'),
    path('add-tempat-kuliner/', add_tempat_kuliner, name='add_tempat_kuliner'),
    path('get-tempat-kuliner/', get_tempat_kuliner, name='get_tempat_kuliner'),
    path('delete-tempat-kuliner/<int:id>', delete_tempat_kuliner, name='delete_tempat_kuliner'),
    path('get-tempat-kuliner-flutter/', show_tempat_kuliner_json, name="show_tempat_kuliner_json"),

    # path("add-tempat-kuliner-flutter/", AddKuliner_flutter, name="AddKuliner_flutter"),
    path('add-data/', add_data, name="add_data"),
    path('delete-data/', delete_data, name="delete_data"),
    path('get-data-by-userid/',get_tempat_kuliner_by_user_id,name="get_tempat_kuliner_by_user_id"),

]
