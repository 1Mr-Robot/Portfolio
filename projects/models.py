from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import os

class ProjectType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        verbose_name = 'Tipo de proyecto'
        verbose_name_plural = 'Tipos de proyectos'

    def __str__(self):
        return self.name
    
class ProjectRole(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        verbose_name = 'Rol en proyecto'
        verbose_name_plural = 'Roles en proyectos'

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título', help_text='Título principal')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug', help_text='Nombre que se mostrará en la URL')
    description = CKEditor5Field('Descripción', config_name='default')
    short_description = models.CharField(max_length=300, verbose_name='Descripción corta', help_text='Texto que se mostrará en la sección de proyectos en la pantalla principal')
    summary = models.CharField(max_length=200, verbose_name='Resumen', help_text='Texto que se mostrará debajo del título en la visualización del proyecto')
    end_date = models.DateField(verbose_name='Fecha de finalización')
    demo_url = models.URLField(blank=True, verbose_name='URL de demo')
    repository_url = models.URLField(blank=True, verbose_name='URL del repositorio')
    project_type = models.ForeignKey(ProjectType, on_delete=models.PROTECT, related_name='projects', verbose_name='Tipo de proyecto')
    project_role = models.ForeignKey(ProjectRole, on_delete=models.PROTECT, related_name='projects', verbose_name='Rol en proyecto')
    duration = models.IntegerField(verbose_name='Duración en meses')
    team_members = models.IntegerField(verbose_name='Número de miembros del equipo')
    og_image = models.ImageField(upload_to='og_images/', null=True, blank=True, verbose_name='Imagen Open Graph', help_text='De preferencia 1200x630 jpg')
    og_alt = models.CharField(max_length=200, null=True, blank=True, verbose_name='Texto Open Graph', help_text='Texto alternativo de la imagen Open Graph')
    active = models.BooleanField(default=True, verbose_name='Activo')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        ordering = ['order']
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

    def __str__(self):
        return self.title

def project_image_path(instance, filename):
    return os.path.join(
        'projects',
        instance.project.slug,
        filename
    )

class ProjectImage(models.Model):
    project = models.ForeignKey('Project', related_name='images', on_delete=models.CASCADE, verbose_name='Proyecto')
    image = models.ImageField(upload_to=project_image_path, verbose_name='Imagen')
    caption = models.CharField(max_length=255, blank=True, verbose_name='Descripción')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        ordering = ['order']
        verbose_name = 'Imagen de proyecto'
        verbose_name_plural = 'Imágenes de proyectos'

    def __str__(self):
        return f"Image for {self.project.title} - {self.caption}"
    
class ProjectCharacteristic(models.Model):
    project = models.ForeignKey('Project', related_name='characteristics', on_delete=models.CASCADE, verbose_name='Proyecto')
    title = models.CharField(max_length=200, verbose_name='Título')
    description = CKEditor5Field('Descripción', config_name='default')
    icon = models.TextField(verbose_name="Ícono", help_text="SVG del ícono")
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        ordering = ['order']
        verbose_name = 'Característica de proyecto'
        verbose_name_plural = 'Características de proyectos'

    def __str__(self):
        return f"{self.title}: {self.description}"
    
class ProjectTechnology(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        verbose_name = 'Tecnología de proyecto'
        verbose_name_plural = 'Tecnologías de proyectos'

    def __str__(self):
        return self.name
    
class ProjectTechnologyLink(models.Model):
    project = models.ForeignKey('Project', related_name='technology_links', on_delete=models.CASCADE, verbose_name='Proyecto')
    technology = models.ForeignKey('ProjectTechnology', related_name='project_links', on_delete=models.CASCADE, verbose_name='Tecnología')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creado')
    modified = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificado')

    class Meta:
        ordering = ['order']
        unique_together = ('project', 'technology')
        verbose_name = 'Enlace de tecnología de proyecto'
        verbose_name_plural = 'Enlaces de tecnologías de proyectos'

    def __str__(self):
        return f"{self.project.title} - {self.technology.name}"