# Generated by Django 3.2.19 on 2023-06-17 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockouter', '0002_auto_20220104_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='financial',
            name='country',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
