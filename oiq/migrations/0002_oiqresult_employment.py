# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtfapp', '0002_employmentrole_code'),
        ('oiq', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oiqresult',
            name='employment',
            field=models.ForeignKey(to='dtfapp.Employment', null=True),
            preserve_default=True,
        ),
    ]
