# Generated by Django 2.2 on 2020-08-13 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagestore', '0002_album_brief'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumupload',
            name='zip_file',
            field=models.FileField(help_text='Select a .zip file of images to upload into a new Gallery.', upload_to='temp/', verbose_name='images file (.zip)'),
        ),
    ]