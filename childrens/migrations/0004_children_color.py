# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('childrens', '0003_auto_20141025_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='children',
            name='color',
            field=models.CharField(max_length=8, null=True, verbose_name='Barva', blank=True),
            preserve_default=True,
        ),
    ]
