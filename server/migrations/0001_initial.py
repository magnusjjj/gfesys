# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', editable=False)),
                ('description', models.TextField()),
                ('questions', models.TextField()),
                ('image', models.ImageField(height_field=b'image_height', width_field=b'image_width', max_length=500, upload_to=b'servers')),
                ('image_height', models.IntegerField()),
                ('image_width', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField()),
                ('role', models.CharField(max_length=200)),
                ('status', models.CharField(default=b'WAITING', max_length=200, choices=[(b'OK', b'Accepted'), (b'WAITING', b'Waiting'), (b'DENIED', b'Denied')])),
                ('sec_edit', models.BooleanField(default=False)),
                ('sec_accept', models.BooleanField(default=False)),
                ('sec_moderator', models.BooleanField(default=False)),
                ('createdon', models.DateTimeField(auto_now_add=True, verbose_name=b'Created on')),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('server', models.ForeignKey(to='server.Server')),
            ],
            options={
                'ordering': ['-sec_accept', '-sec_edit', 'role'],
            },
            bases=(models.Model,),
        ),
    ]
