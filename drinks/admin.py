from django.contrib import admin

from .models import Drink
from .models import DrinkImage


class DrinkImageInline(admin.TabularInline):
    model = DrinkImage

    readonly_fields = ['img_preview']



@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    # exclude = ('uuid',)
    # fields = (,)
    list_display = ['name', 'created_by', 'is_publishable']
    list_filter = ['created_by', 'is_publishable']
    # list_display_links = []
    search_fields = ('name',)
    inlines = [DrinkImageInline]


@admin.register(DrinkImage)
class DrinkImageAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']
