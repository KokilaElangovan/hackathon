# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-23 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_doctorpatientmapping_check_up_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorpatientmapping',
            name='hospital_location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
