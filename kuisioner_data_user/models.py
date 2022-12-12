from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.


class kuisioner(models.Model):
    nama = models.TextField()
    umur = models.IntegerField()
    gender = models.TextField()
    vaksin = models.TextField()
    negara = models.TextField()
    tujuan = models.TextField()
    prov = models.TextField()
    kontak = models.IntegerField()

class Country(models.Model):
    name = models.CharField(max_length=255, default=None)
    code = models.CharField(max_length=255, default=None)

    def __str__(self):
        return str(self.nama)
