from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Project
from core.models import SocialUser

def projects(request):
    return redirect('home')

def project(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, active=True)
    projects = Project.objects.filter(active=True)
    other_projects = Project.objects.filter(active=True).exclude(id=project.id).order_by('?')
    social_users_in_hero = SocialUser.objects.filter(active=True, is_in_hero=True)
    return render(request, 'projects/project.html', {'project': project, 'projects': projects, 'other_projects': other_projects, 'social_users_in_hero': social_users_in_hero})