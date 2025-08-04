from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Estudiante

@receiver(post_save, sender=User)
def create_estudiante_profile(sender, instance, created, **kwargs):
    if created:
        Estudiante.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_estudiante_profile(sender, instance, **kwargs):
    try:
        instance.estudiante.save()
    except Estudiante.DoesNotExist:
        # Si el estudiante no existe (por ejemplo, si se crea un superusuario directamente sin pasar por el flujo de registro)
        # se puede crear aquí o manejar de otra forma.
        # Por ahora, simplemente lo ignoramos si no existe para evitar errores en casos específicos.
        pass
