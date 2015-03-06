# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ForumThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('createdon', models.DateTimeField(auto_now_add=True, verbose_name=b'Created on')),
                ('extid', models.IntegerField()),
                ('modelname', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('content', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('nick', models.CharField(max_length=200)),
                ('birthdate', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=200)),
                ('street', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('country_id', django_countries.fields.CountryField(max_length=2)),
                ('zip', models.CharField(max_length=200)),
                ('careof', models.CharField(max_length=200)),
                ('socialsecuritynumber', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('joinedon', models.DateTimeField(auto_now_add=True, verbose_name=b'Joined on')),
                ('refreshedon', models.DateTimeField(verbose_name=b'Refreshed on')),
                ('image', models.ImageField(height_field=b'image_height', width_field=b'image_width', max_length=500, upload_to=b'members')),
                ('image_height', models.IntegerField()),
                ('image_width', models.IntegerField()),
                ('password_hash', models.CharField(max_length=200)),
                ('password_salt', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('howto', models.TextField()),
                ('rules', models.TextField()),
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
                ('accepted', models.BooleanField(default=False)),
                ('createdon', models.DateTimeField(auto_now_add=True, verbose_name=b'Created on')),
                ('member', models.ForeignKey(to='server.Member')),
                ('server', models.ForeignKey(to='server.Server')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='forumthread',
            name='createdby',
            field=models.ForeignKey(to='server.Member'),
            preserve_default=True,
        ),
    ]
