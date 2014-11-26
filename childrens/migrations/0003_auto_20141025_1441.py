# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('childrens', '0002_auto_20141025_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='children',
            name='sex',
            field=models.CharField(default='F', max_length=1, verbose_name='Pohlav\xed', choices=[(b'F', 'Holka'), (b'M', 'Kluk')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='children',
            name='photo',
            field=models.ImageField(upload_to=b'uploads', null=True, verbose_name='Fotka', blank=True),
            preserve_default=True,
        ),
    ]
