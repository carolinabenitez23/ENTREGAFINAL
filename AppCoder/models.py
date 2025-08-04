from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Profesor(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    email = models.EmailField()

class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    camada = models.IntegerField()

class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    email = models.EmailField()
    fecha_nacimiento = models.DateField(null=True, blank=True)
    dni = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatares/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.avatar and self.user:
            # Generar avatar por defecto con las iniciales del usuario
            initials = ''
            if self.user.first_name and self.user.last_name:
                initials = f'{self.user.first_name[0]}{self.user.last_name[0]}'.upper()
            elif self.user.username:
                initials = self.user.username[0].upper()
            else:
                initials = '?'

            # Crear una imagen en blanco
            img_size = 128
            img = Image.new('RGB', (img_size, img_size), color = (73, 109, 137))
            d = ImageDraw.Draw(img)

            # Intentar cargar una fuente, si no, usar la fuente por defecto
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except IOError:
                font = ImageFont.load_default()

            # Calcular la posición del texto para centrarlo
            tleft, top, right, bottom = d.textbbox((0, 0), initials, font=font)
            text_width = right - tleft
            text_height = bottom - top
            x = (img_size - text_width) / 2
            y = (img_size - text_height) / 2

            d.text((x, y), initials, fill=(255,255,255), font=font)

            # Guardar la imagen en un BytesIO object
            output = BytesIO()
            img.save(output, format='PNG', quality=100)
            output.seek(0)

            # Asignar la imagen al campo avatar
            self.avatar = InMemoryUploadedFile(output, 'ImageField', f'{self.user.username}_avatar.png', 'image/png', sys.getsizeof(output), None)

        super().save(*args, **kwargs)

