# Generated by Django 3.1.1 on 2021-02-02 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0053_auto_20210127_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='cndquestion',
            name='choice_num',
            field=models.PositiveSmallIntegerField(default=5),
        ),
    ]