# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import ReadingsTerm, ReadingsRecord

class ReadingsRecordInline(admin.TabularInline):
    model = ReadingsRecord

class ReadingsTermAdmin(admin.ModelAdmin):
    inlines = [
        ReadingsRecordInline,
    ]


admin.site.register(ReadingsTerm, ReadingsTermAdmin)
