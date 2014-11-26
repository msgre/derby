# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('childrens', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='children',
            name='photo',
            field=models.ImageField(upload_to=b'uploads', verbose_name='Fotka'),
            preserve_default=True,
        ),
    ]
