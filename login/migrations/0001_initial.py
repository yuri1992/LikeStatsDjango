# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('fb_id', models.IntegerField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('birthday', models.CharField(max_length=60, null=True, blank=True)),
                ('first_name', models.CharField(max_length=30, null=True, blank=True)),
                ('last_name', models.CharField(max_length=50, null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True, choices=[(b'm', b'Male'), (b'f', b'Female')])),
                ('link', models.URLField(null=True, blank=True)),
                ('access_token', models.TextField(help_text=b'Facebook token for offline access', null=True, blank=True)),
                ('access_token_expires', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
