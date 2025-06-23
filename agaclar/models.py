from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
from PIL import Image
from django.db import models
import uuid
from django.contrib.auth.models import User
import math
from django.shortcuts import get_object_or_404
from user.models import *
from django.core.files import File
from django.urls import reverse
from django.conf import settings





class Kategori(models.Model):
    isim = models.CharField(max_length=100)

    def __str__(self):
        return self.isim 
    

class Arazi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    isim = models.CharField(max_length=100, null=True)
    arsasahibi = models.ForeignKey(Profile, on_delete=models.CASCADE)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    image = models.FileField(upload_to='araziler/', null=True, blank=True)
    created_at = models.DateTimeField(null=True, verbose_name='olusturulma tarihi', auto_now_add=True)

    def __str__(self):
        return str(self.arsasahibi.user.username) if self.arsasahibi else "Belirtilmemiş"

# Yeni bir alan ekleyerek Profile modeli ile Agac modelini bağlayın
class Konum(models.Model):
    arazi = models.ForeignKey(Arazi, on_delete=models.CASCADE, null=True, default=None)
    lat = models.FloatField(max_length=200000, blank=True, null=True)
    long = models.FloatField(max_length=20000, blank=True, null=True)
    address = models.TextField(default='Bilinmeyen Adres')
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000, default='Content')

    def __str__(self):
        return str(self.title)
    

    
class LatLong(models.Model):
    birlestirme = models.ForeignKey('Birlestirme', on_delete=models.CASCADE, related_name='lat_long_values')
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    
    
    
    def get_konumlar(self):
        return self.birlestirme.all()
    


class Birlestirme(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Images(models.Model):
    image = models.FileField(upload_to='resimler/', null=True, blank=True)
    gps_latitude = models.FloatField(null=True, blank=True)
    gps_longitude = models.FloatField(null=True, blank=True)



class FramePhoto(models.Model):
    fimage = models.ImageField(upload_to='photos/')
    flatitude = models.FloatField(max_length=200000, blank=True, null=True)
    flongitude = models.FloatField(max_length=200000, blank=True, null=True)


class Agac(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    arazi = models.ForeignKey('Arazi', on_delete=models.CASCADE)
    aimage = models.ImageField(upload_to='photos/', null=True, blank=True)
    alatitude = models.FloatField(blank=True, null=True)
    alongitude = models.FloatField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    ozellik = models.TextField(max_length=500, default='Ozellik')
    img_name = models.CharField(max_length=255, blank=True, null=True)
    termal = models.ImageField(upload_to='termal/', null=True, blank=True)
    optik = models.ImageField(upload_to='optik/', null=True, blank=True)
    
    def __str__(self):
        return f'{self.ozellik[:20]} - {self.arazi.isim}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    





 

    

    







 
    

