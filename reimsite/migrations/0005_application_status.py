# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reimsite', '0004_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
