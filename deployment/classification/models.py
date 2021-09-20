from django.db import models

class brain_MRI(models.Model):
    MRI_image = models.ImageField(upload_to='media/images/')