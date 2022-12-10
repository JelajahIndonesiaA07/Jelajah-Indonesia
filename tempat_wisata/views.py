from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from tempat_wisata.models import tempat_wisata_Item
from django.views.decorators.csrf import requires_csrf_token
from tempat_wisata.forms import WisataForm
from django.views.decorators.csrf import csrf_protect

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ObjectDoesNotExist
import json

@login_required(login_url='/tempat_wisata/login/')
def show_tempat_wisata(request):
    user = request.user
    data_tempat_wisata = tempat_wisata_Item.objects.filter(user=user)
    form = WisataForm(request.POST)
    context = {
    'list_data': data_tempat_wisata,
    'form': form,
    }
    return render(request, "tempat_wisata.html", context)

def get_tempat_wisata(request):
    user = request.user
    data_tempat_wisata = serializers.serialize("json", tempat_wisata_Item.objects.filter(user=user))
    return HttpResponse(data_tempat_wisata, content_type="application/json")

@csrf_protect
def add_tempat_wisata(request):
    if request.method == "POST":
        form = WisataForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            response = HttpResponseRedirect(reverse("tempat_wisata:show_tempat_wisata"))
            return response
    else:
        form = WisataForm()

    context = {'form':form}
    return render(request, 'tempat_wisata.html', context)

requires_csrf_token
def delete_tempat_wisata(request, id):
    task = tempat_wisata_Item.objects.get(id=id)
    task.delete()
    return show_tempat_wisata(request)

def show_tempat_wisata_json(request):
    data = tempat_wisata_Item.objects.all()
    return HttpResponse(serializers.serialize("json", data),content_type="application/json")

# flutter
@csrf_protect
def flutter_add_tempat_wisata(request):
    if request.method == "POST":
        form = WisataForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Successfully Add Tempat Wisata!.","status": 200}, status=200)
    else:
        return JsonResponse({"message": "Failed to Add Tempat Wisata!.","status": 401}, status=401)
    return JsonResponse({"message": "Failed to Add Tempat Wisata!.", "status": 401}, status=401)

requires_csrf_token
def flutter_delete_tempat_wisata(request, id):
    task = tempat_wisata_Item.objects.get(id=id)
    task.delete()
    return JsonResponse({"message": "Successfully Delete Tempat Wisata!.", "status": 200}, status=200)

#flutter
@csrf_exempt
def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nama = data['nama_tempat_wisata']
        provinsi = data['provinsi_tempat_wisata']
        deskripsi = data['deskripsi_tempat_wisata']
        user_id = data['user_id']
        user =  User.objects.get(id = user_id)
        # return JsonResponse({"hasil": "test"}, status=200)
        if user is not None:
            if user.is_active:
                new_id = User.objects.get(id = user_id).pk
                try: 
                    wisatas = tempat_wisata_Item.objects.all()
                    if wisatas is not None:
                        last_wisata_id = tempat_wisata_Item.objects.latest("id").pk
                        for wisata in wisatas:
                            if(((wisata.nama_tempat_wisata).lower() == nama.lower()) and (wisata.user == user) ):
                                return JsonResponse({"hasil": "nama wisata sudah ada"}, status=400)
                
                        wisata_baru = tempat_wisata_Item(last_wisata_id+1,new_id, nama, provinsi, deskripsi)
                except ObjectDoesNotExist:
                    last_wisata_id = 1
                    wisata_baru = tempat_wisata_Item(last_wisata_id,new_id, nama, provinsi, deskripsi)
                    # return  JsonResponse({"hasil": "berhasil menambah data wisata baru"}, status=400)    
               
                wisata_baru.save()
                return JsonResponse({"hasil": "nama wisata berhasil dibuat"}, status=200)
                
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
        wisata_id = data['wisata_id']
        try:
            task = tempat_wisata_Item.objects.get(id=wisata_id)
            if task is not None:
                task.delete()
                return JsonResponse({"hasil": "berhasil"}, status=200)
            else:
                return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)
        except ObjectDoesNotExist:
            return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)


@csrf_exempt
def get_tempat_wisata_by_user_id(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            # wisata_id = data['wisata_id']
            user_id = data['user_id']
            try:
                user =  User.objects.get(id = user_id)
                task = tempat_wisata_Item.objects.filter(user=user)
                if task is not None:
                    return HttpResponse(serializers.serialize("json", task),content_type="application/json")
                else:
                    return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)

            except User.DoesNotExist:
                return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)
                # pass