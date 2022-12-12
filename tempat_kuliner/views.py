from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from tempat_kuliner.models import tempat_kuliner_Item
from django.views.decorators.csrf import requires_csrf_token
from tempat_kuliner.forms import KulinerForm

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import json


@login_required(login_url='/tempat_kuliner/login/')
def show_tempat_kuliner(request):
    user = request.user
    data_tempat_kuliner = tempat_kuliner_Item.objects.filter(user=user)
    form = KulinerForm(request.POST)
    context = {
    'list_data': data_tempat_kuliner,
    'form': form,
    }
    return render(request, "tempat_kuliner.html", context)

def get_tempat_kuliner(request):
    user = request.user
    data_tempat_kuliner = serializers.serialize("json", tempat_kuliner_Item.objects.filter(user=user))
    return HttpResponse(data_tempat_kuliner, content_type="application/json")

requires_csrf_token
def add_tempat_kuliner(request):
    if request.method == "POST":
        form = KulinerForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            response = HttpResponseRedirect(reverse("tempat_kuliner:show_tempat_kuliner"))
            return response
    else:
        form = KulinerForm()

    context = {'form':form}
    return render(request, 'tempat_kuliner.html', context)

requires_csrf_token
def delete_tempat_kuliner(request, id):
    task = tempat_kuliner_Item.objects.get(id=id)
    task.delete()
    return show_tempat_kuliner(request)

def show_tempat_kuliner_json(request):
    data = tempat_kuliner_Item.objects.all()
    return HttpResponse(serializers.serialize("json", data),
                        content_type="application/json")

@csrf_exempt

def AddKuliner_flutter(request):
    if request.method == 'POST':
        # newActivity = json.loads(request.body)

        new_Activity = tempat_kuliner_Item.objects.create(
            nama_tempat_kuliner = request.POST['nama_tempat_kuliner'],
            rating_tempat_kuliner = request.POST['rating_tempat_kuliner'],
            lokasi_tempat_kuliner = request.POST['lokasi_tempat_kuliner'],
        )
        new_Activity.save()
    return JsonResponse({"instance": "Tempat Kuliner berhasil ditambah"}, status=200)

@csrf_exempt
def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nama_tempat_kuliner = data['nama_tempat_kuliner']
        rating_tempat_kuliner = data['rating_tempat_kuliner']
        lokasi_tempat_kuliner = data['lokasi_tempat_kuliner']
        user_id = data['user_id']
        user =  User.objects.get(id = user_id)
        # return JsonResponse({"hasil": "test"}, status=200)
        if user is not None:
            if user.is_active:
                new_id = User.objects.get(id = user_id).pk
                try: 
                    kuliners = tempat_kuliner_Item.objects.all()
                    if kuliners is not None:
                        last_kuliner_id = tempat_kuliner_Item.objects.latest("id").pk
                        for kuliner in kuliners:
                            if(((kuliner.nama_tempat_kuliner).lower() == nama_tempat_kuliner.lower()) and (kuliner.user == user) ):
                                return JsonResponse({"hasil": "nama tempat kuliner sudah ada"}, status=400)
                
                        kuliner_baru = tempat_kuliner_Item(last_kuliner_id+1,new_id, nama_tempat_kuliner, rating_tempat_kuliner, lokasi_tempat_kuliner)
                except ObjectDoesNotExist:
                    last_kuliner_id = 1
                    kuliner_baru = tempat_kuliner_Item(last_kuliner_id,new_id, nama_tempat_kuliner, rating_tempat_kuliner, lokasi_tempat_kuliner)
                    # return  JsonResponse({"hasil": "berhasil menambah data kuliner baru"}, status=400)    
               
                kuliner_baru.save()
                return JsonResponse({"hasil": "nama tempat kuliner berhasil dibuat"}, status=200)
                
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
        kuliner_id = data['kuliner_id']
        try:
            task = tempat_kuliner_Item.objects.get(id=kuliner_id)
            if task is not None:
                task.delete()
                return JsonResponse({"hasil": "berhasil"}, status=200)
            else:
                return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)
        except ObjectDoesNotExist:
            return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)


@csrf_exempt
def get_tempat_kuliner_by_user_id(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            # kuliner_id = data['kuliner_id']
            user_id = data['user_id']
            try:
                user =  User.objects.get(id = user_id)
                task = tempat_kuliner_Item.objects.filter(user=user)
                if task is not None:
                    return HttpResponse(serializers.serialize("json", task),content_type="application/json")
                else:
                    return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)

            except User.DoesNotExist:
                return JsonResponse({"hasil": "gagal, data tidak ditemukan"}, status=404)
                # pass