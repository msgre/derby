# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Children',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=20, verbose_name='Jm\xe9no')),
                ('lastname', models.CharField(max_length=40, verbose_name='P\u0159\xedjmen\xed')),
                ('nickname', models.CharField(max_length=40, null=True, verbose_name='P\u0159ezd\xedvka', blank=True)),
                ('photo', models.ImageField(upload_to=None, verbose_name='Fotka')),
            ],
            options={
                'ordering': ['lastname', 'firstname'],
                'verbose_name': 'D\u011bcko',
                'verbose_name_plural': 'D\u011bcka',
            },
            bases=(models.Model,),
        ),
    ]
