import uuid
from django.db import models
from django.urls import reverse

# Create your models here.
class UploadFiles(models.Model):
    id = models.AutoField(primary_key=True)
    file= models.FileField(upload_to='uploads/')

    def get_absolute_url(self):
        return reverse("file_detail", kwargs={"pk": self.pk})
    

# class PdfFiles(models.Model):
#     name = models.CharField(max_length=500, default=None)
#     filepath= models.FileField(upload_to='files/', null=True, verbose_name="")