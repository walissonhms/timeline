# Generated by Django 2.2.24 on 2022-03-10 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_termo_texto_explicativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticia',
            name='texto_busca',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RunSQL(
            ('CREATE FULLTEXT INDEX noticia_textindex ON base_noticia (texto_busca)',),
            ('DROP INDEX noticia_textindex on base_noticia',)
        ),
    ]