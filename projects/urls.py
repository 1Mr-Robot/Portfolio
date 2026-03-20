from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('<slug:project_slug>/', views.project, name='project'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]