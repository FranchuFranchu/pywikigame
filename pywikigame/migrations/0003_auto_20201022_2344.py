# Generated by Django 3.1.1 on 2020-10-22 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pywikigame', '0002_auto_20201022_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='name',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='cookie',
            field=models.TextField(unique=True),
        ),
    ]
