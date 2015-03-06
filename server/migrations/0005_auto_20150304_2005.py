# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_volunteer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='status',
            field=models.CharField(default=b'WAITING', max_length=200, choices=[(b'OK', b'Accepted'), (b'WAITING', b'Waiting'), (b'DENIED', b'Denied')]),
            preserve_default=True,
        ),
    ]
