# Generated by Django 3.1.1 on 2021-02-21 10:16

import content.models.audio_file
import content.models.radical
import django.contrib.postgres.fields
import django.contrib.postgres.operations
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# content.migrations.0036_auto_20210115_1556
# content.migrations.0043_auto_20210123_1540
# content.migrations.0047_data_audio

class Migration(migrations.Migration):

    replaces = [('content', '0001_initial'), ('content', '0002_auto_20201221_0351'), ('content', '0003_auto_20201221_0427'), ('content', '0004_auto_20201221_0503'), ('content', '0005_auto_20201221_0511'), ('content', '0006_auto_20201221_0553'), ('content', '0007_auto_20201221_0930'), ('content', '0008_auto_20201221_0939'), ('content', '0009_auto_20201221_1202'), ('content', '0010_auto_20201221_1205'), ('content', '0011_auto_20201221_1304'), ('content', '0012_auto_20201221_1340'), ('content', '0013_character_archive'), ('content', '0014_auto_20201221_1912'), ('content', '0015_auto_20201221_1914'), ('content', '0016_auto_20201221_1917'), ('content', '0017_auto_20201221_1918'), ('content', '0018_auto_20201221_1918'), ('content', '0019_auto_20201226_1647'), ('content', '0020_auto_20201227_0521'), ('content', '0021_auto_20201227_1610'), ('content', '0022_auto_20201230_0558'), ('content', '0023_auto_20210102_0838'), ('content', '0024_auto_20210102_1057'), ('content', '0025_auto_20210103_1317'), ('content', '0026_auto_20210103_1454'), ('content', '0027_auto_20210103_1612'), ('content', '0028_auto_20210105_0541'), ('content', '0029_auto_20210109_1514'), ('content', '0030_auto_20210109_1526'), ('content', '0031_auto_20210112_1105'), ('content', '0032_auto_20210113_1556'), ('content', '0033_auto_20210114_0855'), ('content', '0034_auto_20210115_0659'), ('content', '0035_auto_20210115_1555'), ('content', '0036_auto_20210115_1556'), ('content', '0037_auto_20210115_1602'), ('content', '0038_auto_20210118_0810'), ('content', '0039_auto_20210118_0906'), ('content', '0040_auto_20210120_1048'), ('content', '0041_auto_20210123_1158'), ('content', '0042_auto_20210123_1517'), ('content', '0043_auto_20210123_1540'), ('content', '0044_audiofile'), ('content', '0045_add_unaccent'), ('content', '0046_auto_20210126_1213'), ('content', '0047_data_audio'), ('content', '0048_auto_20210127_0855'), ('content', '0049_auto_20210127_1143'), ('content', '0050_sentence_audio')]

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, help_text='This is for internal use only, feel free to use it for note taking', max_length=500)),
                ('chinese', models.CharField(max_length=1)),
                ('identifier', models.CharField(blank=True, max_length=10)),
                ('pinyin', models.CharField(max_length=6)),
                ('character_type', models.CharField(max_length=30)),
                ('memory_aid', models.TextField(blank=True, max_length=300)),
            ],
            options={
                'unique_together': {('chinese', 'identifier')},
            },
        ),
        migrations.CreateModel(
            name='CharacterInWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(help_text='This determines the order of the character in the word.')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.character')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Radical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, help_text='This is for internal use only, feel free to use it for note taking', max_length=500)),
                ('chinese', models.CharField(max_length=1, validators=[django.core.validators.RegexValidator('^(([⺀-⿕㆐-㆟㐀-\u4dbf一-鿌豈-節𠀀-𪛖]+)|x)\\Z', 'this need to be either in Chinese or "x"')])),
                ('definition', models.CharField(blank=True, default='TODO', max_length=100)),
                ('identifier', models.CharField(blank=True, max_length=20)),
                ('explanation', models.TextField(blank=True, default='TODO', max_length=200)),
                ('pinyin', models.CharField(blank=True, default='TODO', max_length=20)),
                ('image', models.ImageField(default='default.jpg', upload_to=content.models.radical.path_and_rename)),
                ('is_done', models.BooleanField(default=False)),
                ('archive', models.TextField(blank=True, help_text='This is auto-generated as reference. Read-only', max_length=500)),
            ],
            options={
                'abstract': False,
                'unique_together': {('chinese', 'identifier')},
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, help_text='This is for internal use only, feel free to use it for note taking', max_length=500)),
                ('chinese', models.CharField(max_length=5)),
                ('identifier', models.CharField(blank=True, max_length=10)),
                ('pinyin', models.CharField(max_length=36)),
                ('memory_aid', models.TextField(blank=True, max_length=300)),
                ('characters', models.ManyToManyField(related_name='characters', related_query_name='character', through='content.CharacterInWord', to='content.Character')),
            ],
            options={
                'unique_together': {('chinese', 'identifier')},
            },
        ),
        migrations.CreateModel(
            name='RadicalInCharacter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.FloatField(default=0, help_text='This determines the order of the elements')),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.character')),
                ('radical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.radical')),
                ('radical_type', models.CharField(blank=True, choices=[(None, 'TODO'), ('semantic', 'semantic'), ('phonetic', 'phonetic'), ('both', 'both'), ('neither', 'neither')], max_length=12)),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('character', 'radical', 'order')},
            },
        ),
        migrations.AddField(
            model_name='characterinword',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.word'),
        ),
        migrations.AlterUniqueTogether(
            name='characterinword',
            unique_together={('character', 'word', 'order')},
        ),
        migrations.AlterField(
            model_name='characterinword',
            name='order',
            field=models.SmallIntegerField(help_text='This determines the order of the character in the word.'),
        ),
        migrations.CreateModel(
            name='WordInSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, help_text='This determines the order of the word in the set.')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='character',
            name='radicals',
            field=models.ManyToManyField(related_name='characters', related_query_name='character', through='content.RadicalInCharacter', to='content.Radical'),
        ),
        migrations.AlterField(
            model_name='word',
            name='characters',
            field=models.ManyToManyField(related_name='words', related_query_name='word', through='content.CharacterInWord', to='content.Character'),
        ),
        migrations.CreateModel(
            name='WordSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, help_text='This is for internal use only, feel free to use it for note taking', max_length=500)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('words', models.ManyToManyField(related_name='word_sets', related_query_name='word_set', through='content.WordInSet', to='content.Word')),
                ('is_done', models.BooleanField(default=False)),
                ('archive', models.TextField(blank=True, help_text='This is auto-generated as reference. Read-only', max_length=500)),
            ],
            options={
                'abstract': False,
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='wordinset',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.word'),
        ),
        migrations.AddField(
            model_name='wordinset',
            name='word_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.wordset'),
        ),
        migrations.AlterUniqueTogether(
            name='wordinset',
            unique_together={('word', 'word_set')},
        ),
        migrations.AlterField(
            model_name='character',
            name='character_type',
            field=models.CharField(blank=True, choices=[(None, 'TODO'), ('Ideographic', 'Ideographic'), ('Compound Ideographic', 'Compound Ideographic'), ('Picto-phonetic', 'Picto-phonetic'), ('Loan', 'Loan')], max_length=30),
        ),
        migrations.AlterField(
            model_name='character',
            name='memory_aid',
            field=models.TextField(blank=True, default='TODO', max_length=300),
        ),
        migrations.AlterField(
            model_name='character',
            name='pinyin',
            field=models.CharField(default='TODO', max_length=20),
        ),
        migrations.AlterField(
            model_name='word',
            name='memory_aid',
            field=models.TextField(blank=True, default='TODO', max_length=300),
        ),
        migrations.AlterField(
            model_name='word',
            name='pinyin',
            field=models.CharField(default='TODO', max_length=36),
        ),
        migrations.AddField(
            model_name='character',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='word',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='characterinword',
            name='order',
            field=models.FloatField(default=0, help_text='This determines the order of the elements'),
        ),
        migrations.CreateModel(
            name='DefinitionInCharacter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.FloatField(default=0, help_text='This determines the order of the elements')),
                ('definition', models.CharField(max_length=70)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='definitions', related_query_name='definition', to='content.character')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pinyin', models.CharField(max_length=200)),
                ('chinese', models.CharField(max_length=40)),
                ('translation', models.CharField(max_length=200)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sentences', related_query_name='sentence', to='content.word')),
                ('order', models.FloatField(default=0, help_text='This determines the order of the elements')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AlterField(
            model_name='wordinset',
            name='order',
            field=models.FloatField(default=0, help_text='This determines the order of the elements'),
        ),
        migrations.AlterField(
            model_name='character',
            name='pinyin',
            field=models.CharField(default='TODO', max_length=40),
        ),
        migrations.AlterField(
            model_name='character',
            name='character_type',
            field=models.CharField(blank=True, choices=[(None, 'TODO'), ('pictographic', 'pictographic'), ('Ideographic', 'Ideographic'), ('Compound Ideographic', 'Compound Ideographic'), ('Picto-phonetic', 'Picto-phonetic'), ('Loan', 'Loan')], max_length=30),
        ),
        migrations.AlterField(
            model_name='character',
            name='chinese',
            field=models.CharField(max_length=1, validators=[django.core.validators.RegexValidator('^(([⺀-⿕㆐-㆟㐀-\u4dbf一-鿌豈-節𠀀-𪛖]+)|x)\\Z', 'this need to be either in Chinese or "x"')]),
        ),
        migrations.AlterField(
            model_name='word',
            name='chinese',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^(([⺀-⿕㆐-㆟㐀-\u4dbf一-鿌豈-節𠀀-𪛖]+)|x)\\Z', 'this need to be either in Chinese or "x"')]),
        ),
        migrations.AlterField(
            model_name='character',
            name='character_type',
            field=models.CharField(blank=True, choices=[(None, 'TODO'), ('Pictographic', 'Pictographic'), ('Ideographic', 'Ideographic'), ('Compound Ideographic', 'Compound Ideographic'), ('Picto-phonetic', 'Picto-phonetic'), ('Loan', 'Loan')], max_length=30),
        ),
        migrations.AlterField(
            model_name='character',
            name='memory_aid',
            field=models.TextField(blank=True, default='TODO', max_length=300, verbose_name='word memory aid'),
        ),
        migrations.AlterField(
            model_name='word',
            name='memory_aid',
            field=models.TextField(blank=True, default='TODO', max_length=300, verbose_name='word memory aid'),
        ),
        migrations.AddField(
            model_name='character',
            name='archive',
            field=models.TextField(blank=True, help_text='This is auto-generated as reference. Read-only', max_length=500),
        ),
        migrations.AddField(
            model_name='word',
            name='archive',
            field=models.TextField(blank=True, help_text='This is auto-generated as reference. Read-only', max_length=500),
        ),
        migrations.AlterField(
            model_name='word',
            name='chinese',
            field=models.CharField(max_length=10),
        ),
        migrations.CreateModel(
            name='DefinitionInWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_of_speech', models.CharField(blank=True, choices=[(None, 'N/A'), (' ', 'TODO'), ('adj', 'adjective'), ('adv', 'adverb'), ('conj', 'conjunction'), ('interj', 'interjection'), ('m', 'measure word'), ('mv', 'modal verb'), ('n', 'noun'), ('nu', 'numeral'), ('p', 'particle'), ('pn', 'proper noun'), ('pr', 'pronoun'), ('prefix', 'prefix'), ('prep', 'preposition'), ('qp', 'question particle'), ('qpr', 'question pronoun'), ('t', 'time word'), ('v', 'verb'), ('vc', 'verb plus complement'), ('vo', 'verb plus object')], default=' ', max_length=6)),
                ('definition', models.CharField(blank=True, max_length=200)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='definitions', related_query_name='definition', to='content.word')),
                ('order', models.FloatField(default=0, help_text='This determines the order of the elements')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='wordinset',
            unique_together={('word', 'word_set', 'order')},
        ),
        migrations.AlterModelOptions(
            name='character',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ['id']},
        ),
        migrations.CreateModel(
            name='LinkedField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('field_name', models.CharField(blank=True, max_length=50)),
                ('overwrite', models.CharField(blank=True, max_length=200)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewableObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewable', to='content.character')),
                ('radical', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewable', to='content.radical')),
                ('word', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviewable', to='content.word')),
            ],
        ),
        migrations.CreateModel(
            name='MCQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('num_choices', models.PositiveSmallIntegerField(default=4)),
                ('context_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.linkedfield')),
                ('question_type', models.CharField(blank=True, default='custom', max_length=20)),
                ('context_option', models.CharField(choices=[('NOT', 'Not show'), ('MUST', 'Must show'), ('AUTO', 'Auto')], default='AUTO', max_length=4)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MCChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(choices=[(0, 'Correct'), (100, 'Auto Common Wrong'), (101, 'Common Wrong'), (500, 'Missleading'), (2000, 'Very Missleading')])),
                ('linked_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='content.linkedfield')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', related_query_name='choice', to='content.mcquestion')),
            ],
            options={
                'ordering': ['weight'],
            },
        ),
        migrations.CreateModel(
            name='CNDQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(blank=True, default='custom', max_length=20)),
                ('context_option', models.CharField(choices=[('NOT', 'Not show'), ('MUST', 'Must show'), ('AUTO', 'Auto')], default='AUTO', max_length=4)),
                ('question', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=200)),
                ('context_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.linkedfield')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FITBQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('context_link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.linkedfield')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='content.linkedfield')),
                ('extra_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='content.linkedfield')),
                ('question_type', models.CharField(blank=True, default='custom', max_length=20)),
                ('context_option', models.CharField(choices=[('NOT', 'Not show'), ('MUST', 'Must show'), ('AUTO', 'Auto')], default='AUTO', max_length=4)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeneralQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FITB', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='general_question', to='content.fitbquestion')),
                ('MC', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='general_question', to='content.mcquestion')),
                ('reviewable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='content.reviewableobject')),
                ('CND', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='general_question', to='content.cndquestion')),
            ],
        ),
        migrations.AlterField(
            model_name='definitioninword',
            name='part_of_speech',
            field=models.CharField(blank=True, choices=[(None, 'N/A'), (' ', 'TODO'), ('idiom', 'idiom'), ('adj', 'adjective'), ('adv', 'adverb'), ('conj', 'conjunction'), ('interj', 'interjection'), ('m', 'measure word'), ('mv', 'modal verb'), ('n', 'noun'), ('nu', 'numeral'), ('p', 'particle'), ('pn', 'proper noun'), ('pr', 'pronoun'), ('prefix', 'prefix'), ('prep', 'preposition'), ('qp', 'question particle'), ('qpr', 'question pronoun'), ('t', 'time word'), ('v', 'verb'), ('vc', 'verb plus complement'), ('vo', 'verb plus object')], default=' ', max_length=6),
        ),
        migrations.AddField(
            model_name='cndquestion',
            name='reviewable',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='content.reviewableobject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fitbquestion',
            name='reviewable',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='content.reviewableobject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mcquestion',
            name='reviewable',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='content.reviewableobject'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='character',
            name='memory_aid',
            field=models.TextField(blank=True, default='TODO', max_length=300, verbose_name='character memory aid'),
        ),
        migrations.RenameField(
            model_name='fitbquestion',
            old_name='answer',
            new_name='answer_link',
        ),
        migrations.RenameField(
            model_name='fitbquestion',
            old_name='extra_information',
            new_name='title_link',
        ),
        migrations.AlterField(
            model_name='characterinword',
            name='order',
            field=models.FloatField(default=99, help_text='This determines the order of the elements'),
        ),
        migrations.AlterField(
            model_name='definitionincharacter',
            name='order',
            field=models.FloatField(default=99, help_text='This determines the order of the elements'),
        ),
        migrations.AlterField(
            model_name='definitioninword',
            name='order',
            field=models.FloatField(default=99, help_text='This determines the order of the elements'),
        ),
        migrations.AlterField(
            model_name='radicalincharacter',
            name='order',
            field=models.FloatField(default=99, help_text='This determines the order of the elements'),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='order',
            field=models.FloatField(default=99, help_text='This determines the order of the elements'),
        ),
        migrations.AlterField(
            model_name='wordinset',
            name='order',
            field=models.FloatField(default=99, help_text='This determines the order of the elements'),
        ),
        migrations.AddField(
            model_name='cndquestion',
            name='correct_answers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=5), default=list, size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cndquestion',
            name='title_link',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='content.linkedfield'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cndquestion',
            name='wrong_answers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=5), default=list, size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sentence',
            name='chinese_highlight',
            field=models.CharField(default='', max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sentence',
            name='pinyin_highlight',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sentence',
            name='translation_highlight',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
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
        django.contrib.postgres.operations.UnaccentExtension(
        ),
        migrations.AddField(
            model_name='audiofile',
            name='type',
            field=models.CharField(choices=[('taiwan', 'taiwan'), ('self', 'self recorded')], default='pinyin', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='character',
            name='audio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='characters', related_query_name='character', to='content.audiofile'),
        ),
        migrations.AddField(
            model_name='radical',
            name='audio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='radicals', related_query_name='radical', to='content.audiofile'),
        ),
        migrations.AddField(
            model_name='word',
            name='audio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='words', related_query_name='word', to='content.audiofile'),
        ),
        migrations.AlterModelOptions(
            name='audiofile',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='audiofile',
            name='archive',
            field=models.TextField(blank=True, help_text='This is auto-generated as reference. Read-only', max_length=500),
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='content',
            field=models.TextField(help_text="\n        This field is used for auto searching, and (type, content) must be unique. \n        When type is pinyin, content must be pinyin with tone without any \n        whitespace to either side. When type is word, content must be chinese \n        characters. If you don't want this audio to be matched to a content object \n        automatically, set type to custom. \n        ", max_length=300),
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='origin',
            field=models.CharField(choices=[('taiwan', 'taiwan'), ('baidu', 'baidu'), ('self', 'self recorded')], default='self', max_length=10),
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='type',
            field=models.CharField(choices=[('taiwan', 'taiwan'), ('baidu', 'baidu'), ('self', 'self recorded')], max_length=10),
        ),
        migrations.AlterField(
            model_name='radical',
            name='audio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='radicals', related_query_name='radical', to='content.audiofile'),
        ),
        migrations.AlterUniqueTogether(
            name='audiofile',
            unique_together={('type', 'content')},
        ),
        migrations.AlterField(
            model_name='audiofile',
            name='type',
            field=models.CharField(choices=[('pinyin', 'pinyin'), ('custom', 'custom'), ('word', 'word')], max_length=10),
        ),
        migrations.AddField(
            model_name='sentence',
            name='audio',
            field=models.ForeignKey(default=content.models.audio_file.AudioFile.get_default_pk, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='sentences', related_query_name='sentence', to='content.audiofile'),
        ),
    ]