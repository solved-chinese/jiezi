# Generated by Django 3.1.1 on 2021-01-03 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0026_auto_20210103_1454'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wordinset',
            unique_together={('word', 'word_set', 'order')},
        ),
    ]