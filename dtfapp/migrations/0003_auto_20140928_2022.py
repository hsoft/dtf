# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtfapp', '0002_employmentrole_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employment',
            old_name='start_date',
            new_name='query_date',
        ),
        migrations.RemoveField(
            model_name='employment',
            name='end_date',
        ),
    ]
