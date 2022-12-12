from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers

from django.shortcuts import render
from emergencycall.models import EmergencyCallItem

from emergencycall.forms import HospitalForm

from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import requires_csrf_token
from django.http import JsonResponse
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User




# Create your views here.
@login_required(login_url='/emergencycall/login/')
def show_hospital(request):
    user = request.user
    data_hospital = EmergencyCallItem.objects.filter(user=user)
    form = HospitalForm(request.POST)
    context = {
        'list_hospital': data_hospital,
        'form': form,
    }
    return render(request, "emergencycall.html", context)

def get_hospital(request):
    user = request.user
    data_hospital = serializers.serialize("json", EmergencyCallItem.objects.filter(user=user))
    return HttpResponse(data_hospital, content_type="application/json")

requires_csrf_token
def new_hospital(request):
    if request.method == "POST":
        form = HospitalForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            response = HttpResponseRedirect(reverse("emergencycall:show_hospital"))
            return response
    else:
        form = HospitalForm()

    context = {'form':form}
    return render(request, 'emergencycall.html', context)

def hapus(request, id):
    task = EmergencyCallItem.objects.get(id=id)
    task.delete()
    return show_hospital(request)

def show_hospital_json(request):
    data = EmergencyCallItem.objects.all()
    return HttpResponse(serializers.serialize("json", data),
                        content_type="application/json")

def show_emergencycall_json(request):
    data = EmergencyCallItem.objects.all()
    return HttpResponse(serializers.serialize("json", data),
                        content_type="application/json")

@csrf_exempt
def AddEmergencycall_flutter(request):
    if request.method == 'POST':
        # newActivity = json.loads(request.body)

        new_Activity = EmergencyCallItem.objects.create(
            hospital_name = request.POST['hospital_name'],
            hospital_number = request.POST['hospital_number'],
            hospital_location = request.POST['hospital_location'],
        )

        new_Activity.save()
    return JsonResponse({"instance": "Rumah Sakit berhasil ditambah"}, status=200)


@csrf_exempt
def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nama = data['hospital_name']
        telefon = data['hospital_number']
        lokasi = data['hospital_location']
        user_id = data['user_id']
        user =  User.objects.get(id = user_id)
        # return JsonResponse({"hasil": "test"}, status=200)
        if user is not None:
            if user.is_active:
                new_id = User.objects.get(id = user_id).pk
                try: 
                    hospitals = EmergencyCallItem.objects.all()
                    if hospitals is not None:
                        last_hospital_id = EmergencyCallItem.objects.latest("id").pk
                        for wisata in hospitals:
                            if(((wisata.nama_tempat_wisata).lower() == nama.lower()) and (wisata.user == user) ):
                                return JsonResponse({"hasil": "nama rumah sakit sudah ada"}, status=400)
                
                        wisata_baru = EmergencyCallItem(last_hospital_id+1,new_id, nama, telefon, lokasi)
                except ObjectDoesNotExist:
                    last_hospital_id = 1
                    wisata_baru = EmergencyCallItem(last_hospital_id,new_id, nama, telefon, lokasi)
                    # return  JsonResponse({"hasil": "berhasil menambah data rumah sakit baru"}, status=400)    
               
                wisata_baru.save()
                return JsonResponse({"hasil": "nama rumah sakit berhasil dibuat"}, status=200)
                
                # return JsonResponse({"hasil": "bisa", "user": new_id, "dump": "OK"}, status=200)

        else:
            return JsonResponse({
                "status": False,
                "message": "Failed to Login, Account Disabled."
            }, status=401)


@csrf_exempt
def delete_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        hospital_id = data['hospital_id']
        try:
            task = EmergencyCallItem.objects.get(id=hospital_id)
            if task is not None:
                task.delete()
                return JsonResponse({"hasil": "berhasil"}, status=200)
            else:
                return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)
        except ObjectDoesNotExist:
            return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)


@csrf_exempt
def get_emergencycall_by_user_id(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            # wisata_id = data['wisata_id']
            user_id = data['user_id']
            try:
                user =  User.objects.get(id = user_id)
                task = EmergencyCallItem.objects.filter(user=user)
                if task is not None:
                    return HttpResponse(serializers.serialize("json", task),content_type="application/json")
                else:
                    return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)

            except User.DoesNotExist:
                return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)
                # pass
