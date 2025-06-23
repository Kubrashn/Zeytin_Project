from django.contrib import admin
from .models import *
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms    
    

class LatLongInline(admin.TabularInline):  # veya StackedInline
    model = LatLong
    extra = 3  # Kaç adet giriş alanı gösterileceğini belirleyebilirsiniz


class BirlestirmeAdmin(admin.ModelAdmin):
    inlines = [LatLongInline]



    
class KonumInline(admin.TabularInline):
    model = Konum
    extra = 1



class AraziAdmin(admin.ModelAdmin):
    list_display = ('id', 'arsasahibi', 'kategori', 'created_at')
    search_fields = ('arsasahibi__username', 'kategori__isim')

    fields = ('id', 'arsasahibi', 'image', 'created_at', 'isim', 'kategori' )  # 'created_at' alanını düzenlenebilir hale getiriyoruz

    readonly_fields = ('id', 'created_at')
    inlines = [KonumInline]

class AgacAdmin(admin.ModelAdmin):
    list_display = ('ozellik', 'arazi', 'alatitude', 'alongitude')
    list_filter = ('arazi',)    



admin.site.register(Agac, AgacAdmin)
admin.site.register(Arazi, AraziAdmin)
admin.site.register(Kategori)
admin.site.register(Konum)
admin.site.register(Birlestirme, BirlestirmeAdmin)
admin.site.register(LatLong)
admin.site.register(Images)
admin.site.register(FramePhoto)


