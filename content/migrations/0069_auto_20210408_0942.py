# Generated by Django 3.1.1 on 2021-04-08 09:42

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0068_auto_20210408_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='cndquestion',
            name='is_done',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fitbquestion',
            name='is_done',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mcquestion',
            name='is_done',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fitbquestion',
            name='alternative_answers',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=8), blank=True, default=list, help_text='punctuations and spaces will be ignored, case insensitive', size=None),
        ),
    ]
