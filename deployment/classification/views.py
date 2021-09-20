from classification.models import brain_MRI
from django.shortcuts import redirect, render
import joblib
from .forms import brain_MRI_form
from django.http import HttpResponse


def home(request):
    return render(request, "home.html")

def MRI_image(request):
    if request.method == 'POST':
        #breakpoint()
        form = brain_MRI_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            form = brain_MRI_form()
    else:
        return render(request, 'home.html')

def success(request):
    return HttpResponse('successfully uploaded')


def result(request):
    #model = joblib.load("final_model.sav")

    ##image = request.GET['avatar']
    MRI_image = brain_MRI.objects.all()

    return render(request, 'result.html', {'MRI' : MRI_image})