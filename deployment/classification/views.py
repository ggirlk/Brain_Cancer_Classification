from classification.models import brain_MRI
from django.shortcuts import redirect, render
import joblib
from .forms import brain_MRI_form
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import brain_MRI

def home(request):
    return render(request, "home.html")

def MRI_image(request):
    if request.method == 'POST':
        form = brain_MRI_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('result', form['MRI_image'])
        else:
            form = brain_MRI_form()
    else:
        return render(request, 'home.html')

def success(request):
    return HttpResponse('successfully uploaded')


def result(request, MRI_image):
    #model = joblib.load("final_model.sav")

    ##image = request.GET['avatar']
    breakpoint()
    return render(request, 'result.html')