from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Certificate, SkillCategory, Skill, SocialNetwork, SocialUser

@admin.register(Certificate)
class CertificateAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('id', 'title', 'institution', 'start_date', 'type', 'active', 'order')
    list_filter = ('active', 'type', 'institution')
    search_fields = ('title', 'institution')
    ordering = ('order',)
    date_hierarchy = 'created'
    sortable_by = ('order',)

@admin.register(SkillCategory)
class SkillCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('id', 'name', 'active', 'order')
    list_filter = ('active',)
    search_fields = ('name',)
    ordering = ('order',)
    date_hierarchy = 'created'
    sortable_by = ('order',)

@admin.register(Skill)
class SkillAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('id', 'name', 'category', 'active', 'order')
    list_filter = ('category', 'active',)
    search_fields = ('name', 'category__name')
    ordering = ('order',)
    date_hierarchy = 'created'
    sortable_by = ('order',)

@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('id', 'name', 'base_url')
    search_fields = ('name', 'slug')
    date_hierarchy = 'created'

@admin.register(SocialUser)
class SocialUserAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('id', 'username', 'social_network', 'profile_url', 'active', 'is_in_hero', 'order')
    list_filter = ('social_network', 'active', 'is_in_hero',)
    search_fields = ('username', 'social_network__name')
    ordering = ('order',)
    date_hierarchy = 'created'
    sortable_by = ('order',)