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
from tensorflow.compat.v1 import Session
import tensorflow as tf
import json


model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model = load_model('.models/QModel.h5')


def home(request):
    return render(request, "home.html")

def MRI_image(request):
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
    
    test_file = '.' + filePathName




    img = image.load_img(test_file, target_size=(512, 512))
    x = image.img_to_array(img)

    with model_graph.as_default():
        with tf_session.as_default():
            res = model.predict(x)

    
    import numpy as np
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