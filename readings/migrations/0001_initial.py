# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('childrens', '0002_auto_20141025_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_from', models.DateField(verbose_name='Od')),
                ('date_to', models.DateField(verbose_name='Do')),
                ('minutes', models.IntegerField(help_text='Kolik minut za zadan\xe9 obdob\xed p\u0159e\u010detl(-a)', verbose_name='Minuty')),
                ('note', models.TextField(help_text='T\u0159eba co za kn\xed\u017eky \u010detl(-a)', null=True, verbose_name='Pozn\xe1mka', blank=True)),
                ('children', models.ForeignKey(verbose_name='D\u011bcko', to='childrens.Children')),
            ],
            options={
                'ordering': ['date_from', 'children__lastname', 'children__firstname'],
                'verbose_name': '\u010cten\xed',
                'verbose_name_plural': '\u010cten\xed',
            },
            bases=(models.Model,),
        ),
    ]
