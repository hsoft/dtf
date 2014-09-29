# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtfapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employmentrole',
            name='code',
            field=models.CharField(unique=True, max_length=10, default='table-was-empty-when-this-migration-was-done-not-supposed-to-be-used'),
            preserve_default=False,
        ),
    ]
