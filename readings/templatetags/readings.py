# -*- coding: utf-8 -*-

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_minutes(form, child):
    return form['minutes_%s' % child.id]

@register.filter
def get_add(form, child):
    return form['add_%s' % child.id]

@register.filter
def get_minutes_errors(form, child):
    return mark_safe(form['minutes_%s' % child.id].errors)

@register.filter
def get_add_errors(form, child):
    return mark_safe(form['add_%s' % child.id].errors)
