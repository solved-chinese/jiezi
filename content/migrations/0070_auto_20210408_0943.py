# Generated by Django 3.1.1 on 2021-04-08 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0069_auto_20210408_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cndquestion',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fitbquestion',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mcquestion',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]