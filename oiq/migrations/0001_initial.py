# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtfapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OIQQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date', models.DateField(db_index=True)),
                ('person', models.ForeignKey(to='dtfapp.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OIQResult',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('contactid', models.CharField(unique=True, max_length=100)),
                ('firstname', models.CharField(db_index=True, max_length=100)),
                ('lastname', models.CharField(db_index=True, max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('employer', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=20)),
                ('graduation', models.CharField(max_length=20)),
                ('university', models.CharField(max_length=100)),
                ('speciality', models.CharField(max_length=100)),
                ('query', models.ForeignKey(to='oiq.OIQQuery')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
