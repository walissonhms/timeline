# Generated by Django 2.2.24 on 2022-01-29 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20220128_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='url',
            field=models.URLField(max_length=250, unique=True),
        ),
    ]