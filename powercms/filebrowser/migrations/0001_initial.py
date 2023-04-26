# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-16 11:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField(auto_now=True, verbose_name='Hora')),
                ('object_id', models.TextField(blank=True, null=True, verbose_name='Arquivo')),
                ('action_flag', models.PositiveSmallIntegerField(choices=[(1, 'Adicionado'), (2, 'Editado'), (3, 'Removido')], verbose_name='A\xe7\xe3o')),
                ('change_message', models.TextField(blank=True, verbose_name='Altera\xe7\xe3o')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filebrowser_logentry_set', to=settings.AUTH_USER_MODEL, verbose_name='Usu\xe1rio')),
            ],
            options={
                'ordering': ('-action_time',),
                'verbose_name': 'Hist\xf3rico de Opera\xe7\xf5es',
                'verbose_name_plural': 'Hist\xf3rico de Opera\xe7\xf5es',
            },
        ),
    ]
