import os
import django
import pandas as pd
from django.core.management.base import BaseCommand
from django.core.files import File
from agaclar.models import Agac

# Django ortamını ayarla
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agac_site.settings')
django.setup()

class Command(BaseCommand):
    help = 'Imports images from an Excel file and associates them with trees in the database'

    def handle(self, *args, **kwargs):
        excel_file_path = r'C:\Users\kubra\OneDrive\Masaüstü\agac_site_aris - Copy 2\Kitap 24 (1).xlsx'
        df = pd.read_excel(excel_file_path)
        
        resim_klasoru = r'C:\Users\kubra\OneDrive\Masaüstü\agac_site_aris - Copy 2\deneme'
        resim_dosyalar = os.listdir(resim_klasoru)

        for index, row in df.iterrows():
            img_name = row['Name']  # Dosya uzantısını Excel'den al
            img_file = img_name + '.JPG'  # Dosya adını oluştur

            if img_file in resim_dosyalar:
                coordinates = row['Coordinates'].split(',')
                latitude = float(coordinates[1])
                longitude = float(coordinates[0])

                # Ağaç bulunursa işlemi yap, bulunmazsa atla
                try:
                    agac = Agac.objects.get(alatitude=latitude, alongitude=longitude)
                    
                    # Resmi kaydet
                    img_path = os.path.join(resim_klasoru, img_file)
                    if os.path.exists(img_path):  # Dosyanın var olup olmadığını kontrol et
                        with open(img_path, 'rb') as f:
                            agac.aimage.save(img_file, File(f))
                    
                    # Diğer bilgileri güncelle
                    agac.ozellik = row['Description']
                    agac.save()
                    self.stdout.write(self.style.SUCCESS(f"{img_file} başarıyla yüklendi ve güncellendi."))
                except Agac.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"{img_file} için ağaç bulunamadı."))

        self.stdout.write(self.style.SUCCESS("Eşleşen resimler başarıyla kaydedildi."))
