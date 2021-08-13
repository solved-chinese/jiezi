# Generated by Django 3.1.1 on 2021-08-13 15:48

from django.db import migrations


def forward(apps, schema_editor):
    Class = apps.get_model('classroom', 'Class')
    teacher_name_set = set()
    for klass in Class.objects.all():
        pair = (klass.teacher.pk, klass.name)
        if pair in teacher_name_set:
            print(f'removing {klass.teacher.display_name} {klass.teacher.alias} {klass.name}')
            klass.delete()
        else:
            teacher_name_set.add(pair)


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0009_auto_20210702_1653'),
    ]

    operations = [
        migrations.RunPython(forward, migrations.RunPython.noop)
    ]
