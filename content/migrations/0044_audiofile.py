# Generated by Django 3.1.1 on 2021-01-26 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0043_auto_20210123_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='audio')),
                ('note', models.TextField(blank=True, help_text='This is for internal use only, feel free to use it for note taking', max_length=500)),
                ('content', models.TextField(help_text='This field is used for searching', max_length=300)),
                ('origin', models.CharField(choices=[('taiwan', 'taiwan'), ('self', 'self recorded')], default='self', max_length=10)),
            ],
        ),
    ]