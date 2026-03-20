from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from core.models import SocialUser
from .services.get_og_content import get_og_image_url, get_og_image_alt

def projects(request):
    return redirect('home')

def project(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug, active=True)
    projects = Project.objects.filter(active=True)
    other_projects = Project.objects.filter(active=True).exclude(id=project.id).order_by('?')
    social_users_in_hero = SocialUser.objects.filter(active=True, is_in_hero=True)

    context = {
        'project': project,
        'projects': projects,
        'other_projects': other_projects,
        'social_users_in_hero': social_users_in_hero,
        'og_image_url': get_og_image_url(request, project.og_image),
        'og_image_alt': get_og_image_alt(project.og_alt),
    }

    return render(request, 'projects/project.html', context)