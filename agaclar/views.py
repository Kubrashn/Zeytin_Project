from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from .models import *
from django.views.generic.base import TemplateView
import math
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import plotly.express as px
from PIL import Image
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
import io
import base64




# Create your views here.
def index(request):
    araziler = Arazi.objects.all()
    
    context = {
        'araziler':araziler
    }
    return render(request , 'index.html' , context)

def map_detay(request, arazi_id):
    arazi = get_object_or_404(Arazi, id=arazi_id)
    konumlar = Konum.objects.filter(arazi=arazi)
    bkonumlar = LatLong.objects.all()
    birlesmeler = Birlestirme.objects.all()
    context = {
        'arazi': arazi,
        'konumlar': konumlar,
        'bkonumlar':bkonumlar,
        'birlesmeler': birlesmeler
    }
    return render(request, 'map_detay.html', context)

def save_photo(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        image_data = request.FILES.get('image_data')

        # Save the image to the 'photos/' directory
        image_path = 'photos/' + image_data.name
        with open(image_path, 'wb') as destination:
            for chunk in image_data.chunks():
                destination.write(chunk)

        # Save the FramePhoto object to the database
        frame_photo = FramePhoto.objects.create(flatitude=latitude, flongitude=longitude, fimage=image_path)
        frame_photo.save()

        return JsonResponse({'message': 'Photo saved successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)

def map(request):
    konumlar = Konum.objects.all()
    bkonumlar = LatLong.objects.all()
    birlesmeler = Birlestirme.objects.all()
    resimler = Images.objects.all()
    frame = FramePhoto.objects.all()

    crs = 'EPSG:4326'
    all_geo_dfs = []

    for birlesme in birlesmeler:
        lat_long_values = birlesme.lat_long_values.all()
        if lat_long_values:
            geometry = [Point(xy) for xy in zip(lat_long_values.values_list('long', 'lat'))]
            geo_df = gpd.GeoDataFrame({'name': [birlesme.name] * len(geometry), 'geometry': geometry}, crs=crs)
            all_geo_dfs.append(geo_df)

    combined_geo_df = gpd.GeoDataFrame(pd.concat(all_geo_dfs, ignore_index=True), crs=crs)
    
    fig = px.scatter_geo(combined_geo_df,
                         lat=combined_geo_df.geometry.y,
                         lon=combined_geo_df.geometry.x,
                         title='Place Locations')

    # İşlenmiş veriyi HTML şablonuna gönder
    img_html = fig.to_html()

    # RESIM COORDINATE ALMA 

    def dms_to_decimal(degrees, minutes, seconds):
        decimal_value = degrees + (minutes / 60) + (seconds / 3600)
        return decimal_value

    def get_exif_gps(image_path):
        with Image.open(image_path) as img:
            exif_data = img._getexif()  # EXIF verisini al
            if exif_data and 34853 in exif_data:  # 34853 GPSInfo için etiket
                gps_info = exif_data[34853]  # GPSInfo'yu al
                lat_dms = gps_info[2]  # Latitude DMS formatında
                lon_dms = gps_info[4]  # Longitude DMS formatında
            
                lat_decimal = dms_to_decimal(lat_dms[0], lat_dms[1], lat_dms[2])
                lon_decimal = dms_to_decimal(lon_dms[0], lon_dms[1], lon_dms[2])
            
                return lat_decimal, lon_decimal
        return None, None
    

    def get_gps_coordinates_for_photo(photo_id):
        photo = get_object_or_404(Images, id=photo_id)
        lat, lon = get_exif_gps(photo.image.path)  # Assuming 'image' is the ImageField
        return lat, lon
    
    for photo in resimler:
        lat, lon = get_gps_coordinates_for_photo(photo.id)  # Fotoğrafın GPS koordinatlarını al
        photo.gps_latitude = lat  # GPS latitude'ı güncelle
        photo.gps_longitude = lon  # GPS longitude'u güncelle
        photo.save()  # Kaydedilmiş GPS koordinatlarını güncelle
        


    # #Frameimages
        
    # def upload_photo_view(request):
    #     if request.method == 'POST':
    #         form = FrameImagesForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save()
    #     else:
    #         form = FrameImagesForm()  
    #     return render(request, 'map.html' , {'form':form})          
        
    
    
        
   
    context = {
        'konumlar': konumlar,
        'bkonumlar': bkonumlar,
        'birlesmeler': birlesmeler,
        'resimler': resimler,
        'frame':frame,
    }
    return render(request, 'map.html', context)

def ari_index(request):

    return render(request , 'ari_index.html')

def agac_liste(request, arazi_id):
    arazi = Arazi.objects.get(id=arazi_id)
    agaclar = Agac.objects.filter(arazi=arazi)

    context = {
        'arazi': arazi,
        'agaclar': agaclar,
    }

    return render(request, 'agac_liste.html', context)

def agac_detay(request, agac_id):
    agac = Agac.objects.get(id=agac_id)
    context = {
        'agac': agac,
    }
    return render(request , 'agac_detay.html', context)

def tanıtım(request):
    
    context = {
        
    }
    return render(request , 'tanıtım.html', context)