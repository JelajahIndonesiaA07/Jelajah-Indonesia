from django.urls import path
from .views import get_country, get_json, index, hasil

app_name = "kuisioner_data_user"
urlpatterns = [
    path('', index, name='index'),
    path('hasil', hasil, name='hasil'),
    path('json', get_json, name='json'),
    path('location', get_country, name='get_country'),
]
