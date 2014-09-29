# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtfapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('year', models.IntegerField()),
                ('count', models.IntegerField(default=1)),
                ('amount', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dgeqid', models.IntegerField(null=True)),
                ('person', models.ForeignKey(to='dtfapp.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PartyInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('dgeqid', models.CharField(max_length=16)),
                ('party', models.OneToOneField(to='dtfapp.PoliticalParty')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together=set([('person', 'dgeqid')]),
        ),
        migrations.AddField(
            model_name='contribution',
            name='contributor',
            field=models.ForeignKey(to='dgeq.Contributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contribution',
            name='party',
            field=models.ForeignKey(to='dtfapp.PoliticalParty'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='contribution',
            unique_together=set([('contributor', 'party', 'year')]),
        ),
    ]
