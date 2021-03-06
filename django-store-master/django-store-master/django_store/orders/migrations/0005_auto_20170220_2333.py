# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-20 20:03
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20170220_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='phone_mob',
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
