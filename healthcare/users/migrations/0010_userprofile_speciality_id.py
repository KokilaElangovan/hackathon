# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-25 10:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20171225_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='speciality_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Specialities'),
        ),
    ]