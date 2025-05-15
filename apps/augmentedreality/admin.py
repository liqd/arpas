from django.contrib import admin

from . import models


@admin.register(models.Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ["item"]


@admin.register(models.Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ["name", "scene"]


@admin.register(models.Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ["name", "object"]
