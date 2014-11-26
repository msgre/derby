# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readings', '0002_auto_20141025_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='readingsterm',
            name='length',
            field=models.IntegerField(default=500, help_text='Kolik minut chceme za tento term\xedn p\u0159e\u010d\xedst.', verbose_name='D\xe9lka trat\u011b'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='readingsterm',
            name='note',
            field=models.TextField(help_text='Nepovinn\xfd pokec k cel\xe9mu m\u011bs\xedci.', null=True, verbose_name='Pozn\xe1mka', blank=True),
            preserve_default=True,
        ),
    ]
