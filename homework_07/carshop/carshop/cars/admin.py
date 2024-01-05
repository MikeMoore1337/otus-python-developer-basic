# Register your models here.
# admin / admin

from django.contrib import admin

from .models import Car, Engine


# admin.site.register(Car)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["brand", "model", "engine", "year", "price"]
    list_display_links = ["brand", "model"]


@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ["type"]
    list_display_links = ["type"]
