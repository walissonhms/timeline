# Generated by Django 2.2.24 on 2022-05-03 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20220502_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='origem',
            field=models.IntegerField(choices=[(0, 'Manual'), (1, 'CSV'), (2, 'Arquivo PT'), (3, 'Twitter'), (4, 'Google Acadêmico')], default=0),
        ),
        migrations.AddField(
            model_name='noticia',
            name='visivel',
            field=models.BooleanField(default=True, verbose_name='Visível ao público'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='imagem',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Imagem Local'),
        ),
    ]