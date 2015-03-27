# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='gravatar_type',
            field=models.CharField(default=b'identicon', max_length=20, choices=[(b'identicon', b'A geometric pattern based on an email hash'), (b'monsterid', b"A generated 'monster' with different colors, faces, etc"), (b'wavatar', b'Generated faces with differing features and backgrounds'), (b'retro', b'awesome generated, 8-bit arcade-style pixelated faces')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='use_gravatar',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='image_height',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='image_width',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
