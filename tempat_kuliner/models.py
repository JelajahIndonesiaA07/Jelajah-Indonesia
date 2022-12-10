from django.db import models
from django.contrib.auth.models import User

class tempat_kuliner_Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nama_tempat_kuliner = models.TextField()
    rating_tempat_kuliner = models.CharField(max_length = 10)
    lokasi_tempat_kuliner = models.TextField()