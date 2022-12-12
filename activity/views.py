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

# @csrf_exempt
# def delete_data(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         activity_id = data['activity_id']
#         try:
#             task = Task.object.get(id=activity_id)
#             if task is not None:
#                 task.delete()
#                 return JsonResponse({"hasil": "berhasil"}, status=200)
#             else:
#                 return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)
#         except ObjectDoesNotExist:
#             return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)


@csrf_exempt
def delete_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        activity_id = data['activity_id']
        try:
            task = Task.objects.get(id=activity_id)
            if task is not None:
                task.delete()
                return JsonResponse({"hasil": "berhasil"}, status=200)
            else:
                return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)
        except ObjectDoesNotExist:
            return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)


@csrf_exempt
def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data['title']
        description = data['description']
        user_id = data['user_id']
        user =  User.objects.get(id = user_id)
        # return JsonResponse({"hasil": "test"}, status=200)
        if user is not None:
            if user.is_active:
                new_id = User.objects.get(id = user_id).pk
                try: 
                    activities = Task.objects.all()
                    if activities is not None:
                        last_activity_id = Task.objects.latest("id").pk
                        for activity in activities:
                            if(((activity.title).lower() == title.lower()) and (activity.user == user) ):
                                return JsonResponse({"hasil": "nama activity sudah ada"}, status=400)
                
                        activity_baru = Task(last_activity_id+1,new_id, title, description)
                except ObjectDoesNotExist:
                    last_activity_id = 1
                    activity_baru = Task(last_activity_id,new_id, title, description)
                    # return  JsonResponse({"hasil": "berhasil menambah data wisata baru"}, status=400)    
               
                activity_baru.save()
                return JsonResponse({"hasil": "nama activity berhasil dibuat"}, status=200)
                
                # return JsonResponse({"hasil": "bisa", "user": new_id, "dump": "OK"}, status=200)

        else:
            return JsonResponse({
                "status": False,
                "message": "Failed to Login, Account Disabled."
            }, status=401)

@csrf_exempt
def get_activity_id(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            # wisata_id = data['wisata_id']
            user_id = data['user_id']
            try:
                user =  User.objects.get(id = user_id)
                task = Task.objects.filter(user=user)
                if task is not None:
                    return HttpResponse(serializers.serialize("json", task),content_type="application/json")
                else:
                    return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)

            except User.DoesNotExist:
                return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)
                # pass