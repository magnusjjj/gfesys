# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spirit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='category_object_id',
        ),
        migrations.AddField(
            model_name='topic',
            name='category_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topic',
            name='category_content_type',
            field=models.ForeignKey(default=0, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
    ]
