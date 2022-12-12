from django.shortcuts import render

from kuisioner_data_user.models import Country, kuisioner
from .forms import AssessmentForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers


# Create your views here.

@login_required(login_url='/mainpage/login/')
def index(request):
    form = AssessmentForm(request.POST)

    data = {}

    if (form.is_valid()):
        form.save()
        data['nama'] = form.cleaned_data.get('nama')
        data['status'] = "ok"
        print("okoklh")
        return JsonResponse(data)

    context = {
        'form': form,
    }

    return render(request, 'pertanyaan_kuisioner.html', context)


@login_required(login_url='/mainpage/login/')
def hasil(request):
    return render(request, 'hasil_kuisioner.html')

def get_json(request):
    data_film = kuisioner.objects.all()
    return HttpResponse(serializers.serialize("json", data_film), content_type="application/json")

def get_country(request):
    try:
        countries = Country.objects.all().values()
        
        response = {
            "success": True,
            "content": {
                "countries": list(countries)
            },
            "message": "Countries successfully retrieved!"
        }
        
        return HttpResponse(data=response, status=status.HTTP_200_OK)
    except Exception as e:
        response = {
            "success": False,
            "content": None,
            "message": str(e)
        }
         
        return HttpResponse(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
