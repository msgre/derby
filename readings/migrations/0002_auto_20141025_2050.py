# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('childrens', '0003_auto_20141025_1441'),
        ('readings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadingsRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minutes', models.IntegerField(help_text='Kolik minut za zadan\xe9 obdob\xed p\u0159e\u010detl(-a)', verbose_name='Minuty')),
                ('note', models.TextField(help_text='T\u0159eba co za kn\xed\u017eky \u010detl(-a)', null=True, verbose_name='Pozn\xe1mka', blank=True)),
                ('children', models.ForeignKey(verbose_name='D\u011bcko', to='childrens.Children')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReadingsTerm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_from', models.DateField(verbose_name='Od')),
                ('date_to', models.DateField(verbose_name='Do')),
                ('childrens', models.ManyToManyField(to='childrens.Children', through='readings.ReadingsRecord')),
            ],
            options={
                'ordering': ['date_from'],
                'verbose_name': 'Z\xe1znam o \u010dten\xed',
                'verbose_name_plural': 'Z\xe1znamy o \u010dten\xed',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='reading',
            name='children',
        ),
        migrations.DeleteModel(
            name='Reading',
        ),
        migrations.AddField(
            model_name='readingsrecord',
            name='term',
            field=models.ForeignKey(verbose_name='Term\xedn', to='readings.ReadingsTerm'),
            preserve_default=True,
        ),
    ]
