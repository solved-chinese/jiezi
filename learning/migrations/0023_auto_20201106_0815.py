# Generated by Django 3.1.1 on 2020-11-06 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0022_auto_20201102_0801_squashed_0024_auto_20201102_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scability',
            name='accuracy',
            field=models.FloatField(default=float("nan")),
        ),
        migrations.AlterField(
            model_name='studentcharacter',
            name='accuracy',
            field=models.FloatField(default=float("nan")),
        ),
    ]