# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-20 11:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_list_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='owner',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
