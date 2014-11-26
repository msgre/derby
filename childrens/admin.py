# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Children

class ChildrenAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'nickname', 'photo_flag')
    list_filter = ('sex', )

    def photo_flag(self, obj):
        return bool(obj.photo)
    photo_flag.short_description = 'Má fotku?'
    photo_flag.boolean = True


admin.site.register(Children, ChildrenAdmin)
