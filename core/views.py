from django.shortcuts import render
from django.db.models import Prefetch
from django.contrib.staticfiles import finders
from django.http import FileResponse
from .models import SkillCategory, Skill, SocialUser
from projects.models import Project

def home(request):
    skill_categories = SkillCategory.objects.filter(active=True).prefetch_related(
        Prefetch(
            'skills',
            queryset=Skill.objects.filter(active=True).order_by('order')
        )
    )
    social_users = SocialUser.objects.filter(active=True)
    social_users_in_hero = social_users.filter(is_in_hero=True)
    email = SocialUser.objects.filter(social_network__slug='mail',active=True).first()
    projects = Project.objects.filter(active=True)
    return render(request, 'core/home.html', {
        'skill_categories': skill_categories,
        'social_users': social_users,
        'social_users_in_hero': social_users_in_hero,
        'email': email,
        'projects': projects,
    })

def robots_txt(request):
    path = finders.find('robots.txt')
    return FileResponse(open(path, 'rb'), content_type="text/plain")