# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.text import slugify


FIRSTNAME_KEY = 'childrens:firstnames'
SEX = (
    ('F', u'Holka'),
    ('M', u'Kluk'),
)

class Children(models.Model):
    firstname = models.CharField(u"Jméno", max_length=20)
    lastname  = models.CharField(u"Příjmení", max_length=40)
    nickname  = models.CharField(u"Přezdívka", max_length=40, blank=True, null=True)
    sex       = models.CharField(u"Pohlaví", max_length=1, choices=SEX)
    color     = models.CharField(u"Barva", max_length=8, blank=True, null=True)
    photo     = models.ImageField(u"Fotka", upload_to='uploads', max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["lastname", "firstname"]
        verbose_name = u"Děcko"
        verbose_name_plural = u"Děcka"

    def __unicode__(self):
        if self.nickname:
            return self.nickname
        else:
            out = self.firstname
            fname = slugify(self.firstname)
            if settings.REDIS.zscore(FIRSTNAME_KEY, fname) > 1:
                out = u'%s %s.' % (out, self.lastname[:1]) # NOTE: nedelitelna mezera uvnitr
            return out

    def save(self, *args, **kwargs):
        self.store_firstname_stats()
        return super(Children, self).save(*args, **kwargs)

    def store_firstname_stats(self):
        settings.REDIS.zincrby(FIRSTNAME_KEY, self.firstname, 1)
