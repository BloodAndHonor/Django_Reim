# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reimsite', '0002_auto_20150318_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='date',
            field=models.DateField(verbose_name=b'apply date'),
            preserve_default=True,
        ),
    ]
