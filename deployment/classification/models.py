from django.db import models

class brain_MRI(models.Model):
    MRI_image = models.ImageField(null=True, blank=True, upload_to='images/')