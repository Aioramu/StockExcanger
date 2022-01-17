# Generated by Django 3.2.11 on 2022-01-04 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockouter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financial',
            name='debt',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='financial',
            name='gross_profit',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='financial',
            name='income_after_taxes',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='financial',
            name='net_income',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='financial',
            name='revenue',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='debt_eq',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='ebitda',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='env',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='last_divident',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='net_worth',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='pb',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='pe',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='ps',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='roa',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='roe',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='roi',
            field=models.FloatField(null=True),
        ),
    ]
