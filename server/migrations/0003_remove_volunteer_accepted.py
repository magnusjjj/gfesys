# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20150303_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='accepted',
        ),
    ]
