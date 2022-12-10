from django.urls import path
from activity.views import ShowActivityJakarta
from activity.views import ShowActivityBali
from activity.views import ShowActivityJogja
from activity.views import ShowActivityJabar
from activity.views import ShowActivityJateng
from activity.views import ShowActivityJatim
from activity.views import ShowActivityForms
from activity.views import AddActivity
from activity.views import show_json
from activity.views import hapus
from activity.views import show_activity_json
from activity.views import AddActivity_flutter

app_name = 'activity'

urlpatterns = [
    path('jakarta/', ShowActivityJakarta, name="ShowActivityJakarta"),
    path('bali/', ShowActivityBali, name="ShowActivityBali"),
    path('jogja/', ShowActivityJogja, name="ShowActivityJogja"),
    path('jabar/', ShowActivityJabar, name="ShowActivityJabar"),
    path('jateng/', ShowActivityJateng, name="ShowActivityJateng"),
    path('jatim/', ShowActivityJatim, name="ShowActivityJatim"),
    path("forms/", ShowActivityForms, name="ShowActivityForms"),
    path("submit/", AddActivity, name="AddActivity"),
    path("json/", show_json, name="show_json"),
    path("hapus/<int:id>", hapus, name="hapus"),
    path('get-activity-flutter/', show_activity_json, name="show_activity_json"),
    path("add-activity-flutter/", AddActivity_flutter, name="AddActivity_flutter"),
]