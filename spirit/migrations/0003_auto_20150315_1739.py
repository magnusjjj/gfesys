# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spirit', '0002_auto_20150315_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='category_content_type',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='category_id',
        ),
        migrations.AddField(
            model_name='topic',
            name='category',
            field=models.ForeignKey(default=1, verbose_name='category', to='spirit.Category'),
            preserve_default=False,
        ),
    ]
