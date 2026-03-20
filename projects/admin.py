from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import *

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    ordering = ('order',)

class ProjectCharacteristicInline(admin.TabularInline):
    model = ProjectCharacteristic
    extra = 1
    ordering = ('order',)

class ProjectTechnologyLinkInline(admin.TabularInline):
    model = ProjectTechnologyLink
    extra = 1
    ordering = ('order',)
    autocomplete_fields = ('technology',)

@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('name', 'created', 'modified')
    search_fields = ('name',)
    date_hierarchy = 'created'

@admin.register(ProjectRole)
class ProjectRoleAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('name', 'created', 'modified')
    search_fields = ('name',)
    date_hierarchy = 'created'

@admin.register(Project)
class ProjectAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('title', 'project_type', 'project_role', 'end_date', 'active', 'order')
    list_filter = ('project_type', 'project_role', 'active',)
    search_fields = ('title', 'description', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)
    date_hierarchy = 'created'
    sortable_by = ('order',)
    inlines = [
        ProjectImageInline,
        ProjectCharacteristicInline,
        ProjectTechnologyLinkInline,
    ]

@admin.register(ProjectImage)
class ProjectImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('project', 'caption', 'order')
    search_fields = ('project__title', 'caption')
    ordering = ('order',)
    date_hierarchy = 'created'
    sortable_by = ('order',)

@admin.register(ProjectCharacteristic)
class ProjectCharacteristicAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('project', 'title', 'modified', 'order')
    search_fields = ('project__title', 'title', 'description')
    ordering = ('order',)
    date_hierarchy = 'created'
    sortable_by = ('order',)

@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('name', 'modified')
    search_fields = ('name',)
    date_hierarchy = 'created'

@admin.register(ProjectTechnologyLink)
class ProjectTechnologyLinkAdmin(SortableAdminMixin, admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('project', 'technology', 'modified', 'order')
    search_fields = ('project__title', 'technology__name')
    ordering = ('order',)
    date_hierarchy = 'created'
    sortable_by = ('order',)