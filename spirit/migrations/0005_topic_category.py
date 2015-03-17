# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spirit', '0004_auto_20150315_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='category',
            field=models.ForeignKey(default=0, verbose_name='category', to='spirit.Category'),
            preserve_default=False,
        ),
    ]
