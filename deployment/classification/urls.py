from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name='home'),
    #path("success", views.success, name="success"),
    path("result/", views.result, name="result"),
    path('MRI_image', views.MRI_image, name='MRI')
]+ static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)