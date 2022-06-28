# Generated by Django 2.2.24 on 2022-05-02 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_auto_20220420_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='termo',
            name='id_externo',
        ),
        migrations.AddField(
            model_name='noticia',
            name='pdf_atualizado',
            field=models.BooleanField(default=False, verbose_name='PDF gerado'),
        ),
        migrations.AddField(
            model_name='termo',
            name='slug',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='termo',
            name='visivel',
            field=models.BooleanField(default=True, verbose_name='Visível'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='atualizado',
            field=models.BooleanField(default=False, verbose_name='Texto atualizado'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='revisado',
            field=models.BooleanField(default=False, verbose_name='Texto revisado'),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='url_valida',
            field=models.BooleanField(default=False, verbose_name='URL Válida'),
        ),
    ]