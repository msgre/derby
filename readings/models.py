# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from childrens.models import Children

class ReadingsTerm(models.Model):
    date      = models.DateField(u"Měsíc")
    childrens = models.ManyToManyField(Children, through='ReadingsRecord')
    length    = models.IntegerField(u"Délka tratě", default=500, help_text=u"Kolik minut chceme za tento termín přečíst.")
    note      = models.TextField(u"Poznámka", blank=True, null=True, help_text=u"Nepovinný pokec k celému měsíci.")

    class Meta:
        ordering = ["date"]
        verbose_name = u"Záznam o čtení"
        verbose_name_plural = u"Záznamy o čtení"

    def __unicode__(self):
        return self.date

    def save(self, *args, **kwargs):
        self.date = datetime(self.date.year, self.date.month, 1)
        return super(ReadingsTerm, self).save(*args, **kwargs)

    def get_year_interval(self, date=None):
        date = date or self.date
        if date.month >= 9 and date.month <= 12:
            return (date.year, date.year + 1)
        else:
            return (date.year - 1, date.year)


class ReadingsRecord(models.Model):
    children = models.ForeignKey(Children, verbose_name=u'Děcko')
    term     = models.ForeignKey(ReadingsTerm, verbose_name=u'Termín')
    minutes  = models.IntegerField(u"Minuty", help_text=u"Kolik minut za zadané období přečetl(-a)")
    note     = models.TextField(u"Poznámka", blank=True, null=True, help_text=u"Třeba co za knížky četl(-a)")

    def __unicode__(self):
        return '%s (%s)' % (self.children, self.term)
