# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='parent',
        ),
        migrations.AddField(
            model_name='page',
            name='parent_content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='parent_object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='type',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
    ]
