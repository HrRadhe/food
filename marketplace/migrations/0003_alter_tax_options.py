# Generated by Django 4.1.4 on 2023-01-20 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_tax'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name_plural': 'Tax'},
        ),
    ]