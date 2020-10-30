# Generated by Django 3.1.1 on 2020-10-19 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0016_auto_20201012_1138'),
        ('content', '0003_reviewmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningprocess',
            name='review_manager',
            field=models.ForeignKey(null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='+',
                                    to='content.reviewmanager'),
        ),
    ]
