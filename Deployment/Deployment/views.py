from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
import cv2
import numpy as np
import pennylane as qml
from tensorflow.keras.models import load_model
from timeit import default_timer as timer
from datetime import timedelta
import sys
from django import forms
from django.db import models
from .forms.ClassifyForm import ClassifyForm
from .models.ImgModel import ImgModel


filedir = os.path.join(os.path.dirname(__file__), 'files')
q_model = load_model(filedir+'/QModel.h5')

def index(request):
    context = {}
    context['form'] = ClassifyForm()
    return render(request, "index.html", context)
    #return render(request, 'index.html')

wires=4

dev4 = qml.device("default.qubit", wires=wires)  # define the simulator
@qml.qnode(dev4)
def CONVCircuit(phi, wires, i=0):
    """
    quantum convolution Node
    """
    # parameter
    theta = np.pi / 2

    qml.RX(phi[0] * np.pi, wires=0)
    qml.RX(phi[1] * np.pi, wires=1)
    qml.RX(phi[2] * np.pi, wires=2)
    qml.RX(phi[3] * np.pi, wires=3)

    qml.CRZ(theta, wires=[1, 0])
    qml.CRZ(theta, wires=[3, 2])
    qml.CRX(theta, wires=[1, 0])
    qml.CRX(theta, wires=[3, 2])
    qml.CRZ(theta, wires=[2, 0])
    qml.CRX(theta, wires=[2, 0])

    # Expectation value
    measurement = qml.expval(qml.PauliZ(wires=0))

    return measurement


def QCONV1(X, image_number, image_total, step=2):
    """
    quantum convolutional layer
    """

    #H, W, CH = X.shape
    H, W = X.shape
    step2 = 2
    out = np.zeros(((H//step), (W//step)))
    #progress = 0
    for i in range(0, W, step):
        #print("processing image "+str(image_number)+"/ "+str(image_total)+": "+str(int(((i/W+1))*100))+"% ", end="\r")
        print("processing image "+str(image_number)+"/ "+str(image_total)+": "+str(i)+"px   ", end="\r")
        for j in range(0, H, step):
            # get 2x2 pixels and make them 1D array
            phi = X[i:i+2, j:j+2].flatten()
            # Get Measurement
            measurement = CONVCircuit(phi, len(phi))
            out[i//step, j//step] = measurement

    return out

def classify(request):
    img = np.zeros((1, 1))

    if request.method == "POST":
        form = ClassifyForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get("imgfield")
            obj = ImgModel()
            obj = ImgModel.objects.create(
                                 title = img.name,
                                 img = img
                                 )
            obj.save()
            img = cv2.imread("images/"+img.name, cv2.IMREAD_GRAYSCALE)

    if img.shape[0] < 512 and img.shape[1] < 512:
        return JsonResponse(data={"error": "image should be 512X512"})

    scale_percent = 25 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    
    NorImages = resized/255

    processed = QCONV1(NorImages, 1, 1)
    images = np.asarray([processed])

    yhat = q_model.predict(images)
    yhat = yhat.argmax(axis=1)
    d = {
        "error": "null",
        "yhat": int(yhat[0]),
    }

    return JsonResponse(data=d)
    