import csv
from django.core.management.base import BaseCommand
from agaclar.models import *

class Command(BaseCommand):
    help = 'CSV dosyasını okuyarak Agac modelini günceller'

    def handle(self, *args, **kwargs):
        csv_file_path = 'C:\Users\kubra\OneDrive\Masaüstü\qr_kod\balta arazi agac konum sari (1).csv'

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                img_name = row[0]
                lat = float(row[1].replace('°N', '').strip())
                lon = float(row[2].replace('°E', '').strip())
                direction = row[3]

                try:
                    agac = Agac.objects.get(alatitude=lat, alongitude=lon)
                    agac.img_name = img_name
                    agac.save()
                    self.stdout.write(self.style.SUCCESS(f"{agac.id} - {img_name} ile güncellendi."))
                except Agac.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Lat: {lat}, Lon: {lon} için eşleşen ağaç bulunamadı."))
