from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from activity.models import Task
from .forms import CreateForm
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
@csrf_exempt
def AddActivity_flutter(request):
    if request.method == 'POST':
        # newActivity = json.loads(request.body)

        new_Activity = Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
        )

        new_Activity.save()
    return JsonResponse({"instance": "Activity berhasil ditambah"}, status=200)


def ShowActivityJakarta(request):
    context = {}
    return render(request, "activity.html",context)

def ShowActivityBali(request):
    context = {}
    return render(request, "bali.html",context)

def ShowActivityJogja(request):
    context = {}
    return render(request, "jogja.html",context)

def ShowActivityJabar(request):
    context = {}
    return render(request, "jabar.html",context)

def ShowActivityJateng(request):
    context = {}
    return render(request, "jateng.html",context)

def ShowActivityJatim(request):
    context = {}
    return render(request, "jatim.html",context)

@login_required(login_url='/mainpage/login/')
def ShowActivityForms(request):
    user = request.user
    forms_item = Task.objects.filter(user= user)
    form = CreateForm(request.POST)
    context = {
        'list_activity': forms_item,
        'form': form,
    }
    return render(request, "forms.html",context)

requires_csrf_token
def AddActivity(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            response = HttpResponseRedirect(reverse("activity:ShowActivityForms"))
            return response
    else:
        form = CreateForm()

    context = {'form':form}
    return render(request, 'forms.html', context)




def show_json(request):
    user= request.user
    data = serializers.serialize("json", Task.objects.filter(user=user))
    return HttpResponse(data, content_type="application/json")


def hapus(request, id):
    data = Task.objects.get(id=id)
    data.delete()
    return  ShowActivityForms(request)

def show_activity_json(request):
    data = Task.objects.all()
    return HttpResponse(serializers.serialize("json", data),
                        content_type="application/json")

@csrf_exempt
def delete_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        activity_id = data['activity_id']
        try:
            task = Task.get(id=activity_id)
            if task is not None:
                task.delete()
                return JsonResponse({"hasil": "berhasil"}, status=200)
            else:
                return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)
        except ObjectDoesNotExist:
            return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)