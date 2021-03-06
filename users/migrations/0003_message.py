# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-10 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_banner_emailverifyrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='\u7559\u8a00\u8005')),
                ('email', models.EmailField(max_length=50, verbose_name='\u7559\u8a00\u8005\u90ae\u7bb1')),
                ('message', models.CharField(max_length=500, verbose_name='\u7559\u8a00\u4fe1\u606f')),
            ],
            options={
                'verbose_name': '\u7559\u8a00\u677f',
                'verbose_name_plural': '\u7559\u8a00\u677f',
            },
        ),
    ]
