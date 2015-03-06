# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_remove_volunteer_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='status',
            field=models.CharField(default=b'NOTACCEPTED', max_length=200),
            preserve_default=True,
        ),
    ]
