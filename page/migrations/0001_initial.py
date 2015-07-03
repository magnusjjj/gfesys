# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('type', models.CharField(default=b'', max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', unique_with=(b'parent_object_id', b'parent_content_type'), editable=False)),
                ('parent_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('parent_content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'')),
                ('page', models.ForeignKey(to='page.Page')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
