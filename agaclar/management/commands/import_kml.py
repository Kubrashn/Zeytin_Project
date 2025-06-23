from django.core.management.base import BaseCommand
from agaclar.models import Agac, Arazi
import xml.etree.ElementTree as ET
import uuid
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

class Command(BaseCommand):
    help = 'Imports trees from a KML file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('kml_file_path', type=str, help='The path to the KML file.')
        parser.add_argument('arazi_id', type=str, help='The ID of the Arazi.')

    def handle(self, *args, **kwargs):
        kml_file_path = kwargs['kml_file_path']
        arazi_id = kwargs['arazi_id']
        self.import_kml_to_db(kml_file_path, arazi_id)

    def import_kml_to_db(self, kml_file_path, arazi_id):
        try:
            arazi = Arazi.objects.get(id=uuid.UUID(arazi_id))
        except Arazi.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Arazi with ID {arazi_id} does not exist.'))
            return

        tree = ET.parse(kml_file_path)
        root = tree.getroot()

        namespace = {'ns': 'http://www.opengis.net/kml/2.2'}
        count = 1

        for placemark in root.findall(".//ns:Placemark", namespace):
            coordinates_text = placemark.find(".//ns:coordinates", namespace).text.strip()
            name = placemark.find(".//ns:name", namespace).text.strip()
            description_element = placemark.find(".//ns:description", namespace)
            description = description_element.text.strip() if description_element is not None else "No description"

            coordinates_text = coordinates_text.replace('°E', '').replace('°N', '').replace(' ', '')

            try:
                longitude, latitude, _ = map(float, coordinates_text.split(","))

                agac = Agac(
                    id=uuid.uuid4(),
                    arazi=arazi,
                    alatitude=latitude,
                    alongitude=longitude,
                    ozellik=description
                )

                # Create a QR code for the tree
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr_url = f"http://ariarge.com/agac_detay/{agac.id}"
                qr.add_data(qr_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

                # Create the number (E1, E2, E3, etc.) for the left side
                number_text = f"E{count}"
                draw = ImageDraw.Draw(img)
                
                # Set font for the number
                try:
                    number_font = ImageFont.truetype("arial.ttf", 40)
                except IOError:
                    number_font = ImageFont.load_default()

                # Calculate the size of the number to be drawn
                number_width, number_height = draw.textbbox((0, 0), number_text, font=number_font)[2:4]

                # Position the number (left side of the QR code)
                number_x = 10  # A small margin to the left
                number_y = (img.height - number_height) // 2  # Centered vertically

                # Add the number on the left of the QR code
                img_with_number = Image.new('RGB', (img.width + number_width + 20, img.height), (255, 255, 255))
                img_with_number.paste(img, (number_width + 20, 0))

                # Draw the number
                draw_number = ImageDraw.Draw(img_with_number)
                draw_number.text((number_x, number_y), number_text, font=number_font, fill="black")

                # Add a circle around the number
                circle_radius = 50  # Circle size
                circle_center = (number_x + number_width // 2, number_y + number_height // 2)
                draw_number.ellipse(
                    [circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                     circle_center[0] + circle_radius, circle_center[1] + circle_radius],
                    fill="black"
                )

                # Add the number (E1, E2, etc.) in white color inside the circle
                number_in_circle_x = circle_center[0] - number_width // 2  # Centered horizontally
                number_in_circle_y = circle_center[1] - number_height // 2  # Centered vertically
                draw_number.text(
                    (number_in_circle_x, number_in_circle_y),
                    number_text,
                    font=number_font,
                    fill="white"  # White color for text inside the circle
                )

                # Save the image with number and QR code
                buffer = BytesIO()
                file_name = f"qrcode_{agac.id}-{number_text}.png"
                img_with_number.save(buffer, format="PNG")
                agac.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

                agac.sira = int(number_text[1:])  # Store the number as the order (E1 -> 1)
                agac.save()

                count += 1
                self.stdout.write(self.style.SUCCESS(f'Successfully added tree {number_text}'))
            except ValueError as e:
                self.stdout.write(self.style.ERROR(f'Error processing coordinates: {coordinates_text} ({e})'))
