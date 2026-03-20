import os
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
from .models import Project, ProjectImage
from .services.og_image_processing import process_og_image

@receiver(post_save, sender=Project)
def procesar_og_image(sender, instance, created, **kwargs):
    '''
    Procesa la OG image del modelo Project. Checa si es JPG y 1200x630, y si no, la convierte en ese formato.
    '''
    if not instance.og_image:
        return

    # Evitar loops infinitos
    if getattr(instance, "_processing", False):
        return

    instance._processing = True

    old_image = None

    if not created:
        try:
            old = Project.objects.get(pk=instance.pk)
            old_image = old.og_image
        except Project.DoesNotExist:
            pass

    # Procesar imagen
    content_file = process_og_image(instance.og_image)

    filename = f"{slugify(instance.title)}.jpg"

    instance.og_image.save(filename, content_file, save=False)

    # Guardar sin volver a disparar lógica innecesaria
    instance.save(update_fields=['og_image'])

    # Eliminar imagen anterior
    if old_image and old_image != instance.og_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)

    instance._processing = False

@receiver(pre_save, sender=ProjectImage)
def convert_image_to_webp(sender, instance, **kwargs):
    '''
    Procesa las imagenes del modelo Project paraconvertirlas a WEBP.
    '''
    if not instance.image:
        return

    try:
        img = Image.open(instance.image)

        # Convertir a RGB si es necesario
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=85)
        buffer.seek(0)

        # Nombre sin extensión
        name = os.path.splitext(instance.image.name)[0]

        # IMPORTANTE: evitar duplicados infinitos
        if not instance.image.name.endswith(".webp"):
            instance.image.save(
                f"{name}.webp",
                ContentFile(buffer.read()),
                save=False
            )

    except Exception as e:
        print("Error procesando imagen:", e)