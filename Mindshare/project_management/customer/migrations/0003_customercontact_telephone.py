# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-18 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_remove_customercontact_telephone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customercontact',
            name='telephone',
            field=models.CharField(max_length=20, null=True, verbose_name='contact telephone'),
        ),
    ]
