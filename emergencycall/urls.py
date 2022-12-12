from django.urls import path

from emergencycall.views import show_hospital, get_hospital, new_hospital, hapus, show_hospital_json, show_emergencycall_json, AddEmergencycall_flutter
from emergencycall.views import add_data
from emergencycall.views import delete_data
from emergencycall.views import get_emergencycall_by_user_id

app_name = 'emergencycall'

urlpatterns = [
    path('show-hospital/', show_hospital, name='show_hospital'),
    path('get-hospital/', get_hospital, name='get_hospital'),
    path('new-hospital/', new_hospital, name="new_hospital"),
    path('hapus/<int:id>', hapus, name='hapus'),
    path('get-hospital-flutter/', show_hospital_json, name="show_hospital_json"),
    path('get-emergencycall-flutter/', show_emergencycall_json, name="show_emergencycall_json"),
    path("add-emergencycall-flutter/", AddEmergencycall_flutter, name="AddEmergencycall_flutter"),


    path('add-data/', add_data, name="add_data"),
    path('delete-data/', delete_data, name="delete_data"),
    path('get-data-by-userid/',get_emergencycall_by_user_id,name="get_emergencycall_by_user_id"),

]