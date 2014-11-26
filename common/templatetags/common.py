# -*- coding: utf-8 -*-

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def inject_class(field):
    return mark_safe(unicode(field).replace(' id=', ' class="form-control" id='))
