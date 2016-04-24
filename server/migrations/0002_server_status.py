# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='status',
            field=models.IntegerField(default=3, choices=[(1, b'Live'), (2, b'Testing'), (3, b'Draft')]),
            preserve_default=True,
        ),
    ]
