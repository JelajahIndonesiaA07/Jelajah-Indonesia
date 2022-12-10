from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from tempat_kuliner.models import tempat_kuliner_Item
from django.views.decorators.csrf import requires_csrf_token
from tempat_kuliner.forms import KulinerForm
from django.contrib.auth.models import User
from django.http import JsonResponse
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
def add_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nama = data['nama_tempat_kuliner']
        rating = data['rating_tempat_kuliner']
        lokasi = data['lokasi_tempat_kuliner']
        user_id = data['user_id']
        user =  User.objects.get(id = user_id)
        # return JsonResponse({"hasil": "test"}, status=200)
        if user is not None:
            if user.is_active:
                new_id = User.objects.get(id = user_id).pk
                kuliners = tempat_kuliner_Item.objects.all()
                last_kuliner_id = tempat_kuliner_Item.objects.latest("id").pk
                # Redirect to a success page.
                
                for kuliner in kuliners:
                    if(((kuliner.nama_tempat_kuliner).lower() == nama.lower()) and (kuliner.user == user) ):
                        return JsonResponse({"hasil": "nama wisata sudah ada"}, status=400)
            
                kuliner_baru = tempat_kuliner_Item(last_kuliner_id+1,new_id, nama, rating, lokasi)
                
                kuliner_baru.save()
                # return JsonResponse({"hasil": "nama wisata berhasil dibuat"}, status=200)
                
                return JsonResponse({"hasil": "bisa", "user": new_id, "dump": "OK"}, status=200)

        else:
            return JsonResponse({
                "status": False,
                "message": "Failed to Login, Account Disabled."
            }, status=401)
