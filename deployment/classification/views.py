from classification.models import brain_MRI
from django.shortcuts import redirect, render
from .forms import brain_MRI_form
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import brain_MRI
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow import Graph
import tensorflow as tf
import cv2
import numpy as np
import pennylane as qml
import json
import matplotlib as plt
import numpy as np




model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model = load_model('./models/QModel.h5')


def home(request):
    return render(request, "home.html")

def MRI_image(request):
    #Get uploaded image's path
    print("request is: {}".format(request))
    print("_____________________")
    print(request.POST.dict())
    print("_____________________")
    fileObj = request.FILES['MRI_image']
    print(fileObj)
    print("_____________________")
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    print("path: {}".format(filePathName))
    print("_____________________")
    

    testfile = '.' + filePathName
    # Reading the image
    img = cv2.imread(testfile, cv2.IMREAD_GRAYSCALE)
    print("ShAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPE")
    print(img.shape)

    #preprocessing the image with Quantum convolutional node
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

        H, W = X.shape
        step2 = 2
        out = np.zeros(((H//step), (W//step)))
        for i in range(0, W, step):
            print("processing image "+str(image_number)+"/ "+str(image_total)+": "+str(i)+"px   ", end="\r")
            for j in range(0, H, step):
                phi = X[i:i+2, j:j+2].flatten()
                # Get Measurement
                measurement = CONVCircuit(phi, len(phi))
                out[i//step, j//step] = measurement

        return out

    scale_percent = 25 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    #resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    NorImages = resized/255

    processed = QCONV1(NorImages, 1, 1)
    img = np.stack((processed,), axis=-1)

    img = np.asarray([img])


    with model_graph.as_default():
        with tf_session.as_default():
            res = model.predict(img)
    
    
    
    content = {'imagePath': filePathName, 'predicted_res': res}



    if request.method == 'POST':
        form = brain_MRI_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'result.html', content)
        else:
            form = brain_MRI_form()
            print('HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEERREEEEEEEEE')
            return render(request, 'result.html', content)
    else:
        return render(request, 'result.html', content)

def result(request):
    
    return render(request, 'result.html')