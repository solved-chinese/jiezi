# Generated by Django 3.1.1 on 2020-10-28 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_reviewmanager'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewmanager',
            old_name="use_<class 'content.reviews.DefinitionFITB'>",
            new_name='use_DefinitionFITB',
        ),
        migrations.RenameField(
            model_name='reviewmanager',
            old_name="use_<class 'content.reviews.DefinitionMCAnswerCharacter'>",
            new_name='use_DefinitionMCAnswerCharacter',
        ),
        migrations.RenameField(
            model_name='reviewmanager',
            old_name="use_<class 'content.reviews.DefinitionMCAnswerField'>",
            new_name='use_DefinitionMCAnswerField',
        ),
        migrations.RenameField(
            model_name='reviewmanager',
            old_name="use_<class 'content.reviews.DefinitionTOF'>",
            new_name='use_DefinitionTOF',
        ),
        migrations.RenameField(
            model_name='reviewmanager',
            old_name="use_<class 'content.reviews.PinyinFITB'>",
            new_name='use_PinyinFITB',
        ),
        migrations.RenameField(
            model_name='reviewmanager',
            old_name="use_<class 'content.reviews.PinyinMC'>",
            new_name='use_PinyinMC',
        ),
        migrations.RenameField(
            model_name='reviewmanager',
            old_name="use_<class 'content.reviews.PinyinTOF'>",
            new_name='use_PinyinTOF',
        ),
    ]
