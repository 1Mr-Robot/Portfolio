from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from .validators import validate_base_url

class Certificate(models.Model):
    TYPES = [
        ('course', 'Curso'),
        ('diploma', 'Diplomado'),
        ('certification', 'Certificación'),
    ]

    title = models.CharField(max_length=100, verbose_name="Título")
    institution = models.CharField(max_length=100, verbose_name="Institución")
    url = models.URLField(max_length=255, verbose_name="URL del certificado")
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(blank=True, null=True, verbose_name="Fecha de fin")
    type = models.CharField(max_length=20, choices=TYPES, verbose_name="Tipo de certificado")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    image = models.ImageField(upload_to='certificates/', verbose_name="Imagen del certificado")
    active = models.BooleanField(default=True, verbose_name='¿Activo?')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        ordering = ['order']
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"

    def __str__(self):
        return f"{self.title} - {self.institution}"

class SkillCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Categoría")
    active = models.BooleanField(default=True, verbose_name='¿Activo?')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        ordering = ['order']
        verbose_name = "Categoría de habilidad"
        verbose_name_plural = "Categorías de habilidades"

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = CKEditor5Field('Descripción', config_name='default')
    icon = models.TextField(verbose_name="Ícono", help_text="SVG del ícono")
    category = models.ForeignKey(SkillCategory, on_delete=models.PROTECT, related_name='skills', verbose_name="Categoría")
    active = models.BooleanField(default=True, verbose_name='¿Activo?')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        ordering = ['order']
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"

    def __str__(self):
        return self.name

class SocialNetwork(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug', help_text='Se usará para el icono de la red social. Debe estar en minúsculas y con guión bajo.')
    base_url = models.CharField(max_length=255, validators=[validate_base_url], verbose_name='Enlace')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        verbose_name = 'Red Social'
        verbose_name_plural = 'Redes Sociales'

    def __str__(self):
        return self.name

class SocialUser(models.Model):
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.PROTECT, verbose_name='Red Social')
    username = models.CharField(max_length=50, verbose_name='Nombre de usuario')
    profile_url = models.CharField(max_length=100, verbose_name='Path del perfil', help_text='Se usará para el link del perfil. Debe estar en minúsculas y con guión bajo.')
    text = models.CharField(max_length=100, verbose_name='Texto')
    additional_info = models.CharField(max_length=100, blank=True, verbose_name='Información adicional')
    active = models.BooleanField(default=True, verbose_name='¿Activo?')
    is_in_hero = models.BooleanField(default=False, verbose_name='¿Mostrar en el hero?')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        ordering = ['order']
        verbose_name = 'Usuario de red social'
        verbose_name_plural = 'Usuarios de redes sociales'

    def __str__(self):
        return f"{self.username} en {self.social_network.name}"