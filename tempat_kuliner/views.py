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