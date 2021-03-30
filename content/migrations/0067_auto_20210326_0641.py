# Generated by Django 3.1.1 on 2021-03-26 06:41

from django.db import migrations


def forward(apps, schema_editor):
    CNDQuestion = apps.get_model('content', 'CNDQuestion')
    CNDQuestion.objects.update(
        description='Click the correct characters into the right order')


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0066_merge_20210326_0640'),
    ]

    operations = [
        migrations.RunPython(forward, backward, elidable=True)
    ]