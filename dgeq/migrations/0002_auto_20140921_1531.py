# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dgeq', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contribution',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=7),
            preserve_default=True,
        ),
    ]
