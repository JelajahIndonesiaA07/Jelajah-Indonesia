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
