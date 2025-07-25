from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='isim', null=True)
    surname = models.CharField(max_length=100, verbose_name='Soyisim', null=True)
    bio = models.TextField(max_length=500, verbose_name='Hakkinda', default='Merhaba', null=True)
    image = models.FileField(upload_to='profiles/', null=True, verbose_name='Profil Resmi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Olusturulma Tarihi', null=True)

    def __str__(self):
        return self.user.username