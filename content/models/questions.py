from uuid import uuid4
import logging
import numpy as np
import re

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import reverse
from django_better_admin_arrayfield.models.fields import ArrayField


logger = logging.getLogger(__name__)


class GeneralQuestion(models.Model):
    reviewable = models.ForeignKey('ReviewableObject',
                                   on_delete=models.CASCADE,
                                   related_name='questions')
    order = models.PositiveSmallIntegerField()
    MC = models.OneToOneField('MCQuestion', blank=True, null=True,
                              on_delete=models.CASCADE,
                              related_name='general_question')
    FITB = models.OneToOneField('FITBQuestion', blank=True, null=True,
                                on_delete=models.CASCADE,
                                related_name='general_question')
    CND = models.OneToOneField('CNDQuestion', blank=True, null=True,
                                on_delete=models.CASCADE,
                                related_name='general_question')

    class Meta:
        ordering = ('order',)
        unique_together = ('reviewable', 'order')

    def clean(self):
        """ make sure there is only one concrete review question """
        super().clean()
        i = iter([self.MC, self.FITB, self.CND])
        if not any(i) or any(i):
            raise ValidationError(
                f"MC {self.MC} FITB {self.FITB} CND {self.CND} "
                f"not only one exists")
        if self.reviewable != self.concrete_question.reviewable:
            raise ValidationError("self reviewable not same as concrete "
                                  "question reviewable")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def concrete_question(self):
        return self.MC or self.FITB or self.CND

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"<Q{self.id}:{self.concrete_question}>"

    def __getattr__(self, item):
        """ redirects requests to concrete question """
        allowed_delegations = ('render', 'check_answer', 'question_form',
                               'question_type', 'get_admin_url',
                               'get_absolute_url', 'is_done')
        if item in allowed_delegations:
            return getattr(self.concrete_question, item)
        return super().__getattribute__(item)


class BaseConcreteQuestion(models.Model):
    class ContextOption(models.TextChoices):
        NOT_SHOW = 'NOT', 'Not show'
        MUST_SHOW = 'MUST', 'Must show'
        AUTO = 'AUTO', 'Auto'

    question_form = None
    reviewable = models.ForeignKey('ReviewableObject',
                                   on_delete=models.CASCADE,
                                   related_name='+')
    question_type = models.CharField(
        max_length=20, blank=True, default="custom")
    context_link = models.ForeignKey('LinkedField',
                                     on_delete=models.SET_NULL,
                                     null=True, blank=True)
    context_option = models.CharField(max_length=4,
                                      choices=ContextOption.choices,
                                      default=ContextOption.AUTO)
    question = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def render(self, show_all_options=False):
        try:
            concrete_content = self._render(show_all_options=show_all_options)
        except ValidationError:
            logger.critical(f"CONTENT_ERROR: question %r invalid, self delete",
                            self, exc_info=True)
            self.delete()
            raise
        client_dict = {
            'question': self.question,
            **concrete_content
        }
        context = self.context
        if self.context_option == self.ContextOption.MUST_SHOW:
            if not context:
                raise ValueError("must show context but no context found")
        elif self.context_option == self.ContextOption.NOT_SHOW:
            context = None
        if context:
            client_dict['context'] = context
        return {
            'id': uuid4().hex,  # FIXME legacy in frontend, remove soon
            'form': self.question_form,
            'content': client_dict
        }

    @property
    def context(self):
        if self.context_link is None:
            return None
        return self.context_link.value

    def get_general_question(self, order=None):
        try:
            return self.general_question
        except ObjectDoesNotExist:
            if order is None:
                raise ValueError("creating general_question, "
                                 "must specify order")
            kwargs = {
                'reviewable': self.reviewable,
                'order': order,
                self.question_form: self
            }
            return GeneralQuestion.objects.create(**kwargs)

    def get_admin_url(self):
        app = self._meta.app_label
        model = self._meta.model_name
        return reverse(f'admin:{app}_{model}_change', args=(self.id,))

    def get_absolute_url(self):
        return reverse('question_display',
                       args=(self.get_general_question().pk,))

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"<{self.question_form}{self.id}: " \
               f"{self.question_type} on {self.reviewable}>"


class LinkedField(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    field_name = models.CharField(max_length=50, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    overwrite = models.CharField(max_length=200, blank=True)

    @property
    def value(self):
        if self.overwrite:
            return self.overwrite
        try:
            value = getattr(self.content_object, self.field_name)
        except AttributeError:
            logger.error("%r link broken with AttributeError, self delete", self)
            self.delete()
            return None
        if not value:
            logger.error("CONTENT_ERROR: %r has falsy value, self delete", self)
            self.delete()
            return None
        return value

    def clean(self):
        if self.overwrite and self.object_id:
            raise ValidationError("can't have overwrite and object both exist")
        if not self.overwrite and not self.object_id:
            raise ValidationError("can't have overwrite and object both blank")

    @classmethod
    def of(cls, object, field_name):
        content_type = ContentType.objects.get_for_model(object)
        object_id = object.id
        return cls.objects.create(content_type=content_type,
                                  object_id=object_id,
                                  field_name=field_name)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.overwrite:
            return f"<overwritten: {self.overwrite}>"
        try:
            value = getattr(self.content_object, self.field_name)
        except Exception:
            value = None
        return f"<{repr(self.content_object)}'s {self.field_name}: {value}>"


class MCChoice(models.Model):
    class WeightType(models.IntegerChoices):
        CORRECT = 0
        AUTO_COMMON_WRONG = 100
        COMMON_WRONG = 101
        MISSLEADING = 500
        VERY_MISSLEADING = 2000

    linked_value = models.ForeignKey(LinkedField,
                                     on_delete=models.CASCADE,
                                     related_name='+')
    weight = models.PositiveSmallIntegerField(choices=WeightType.choices)
    question = models.ForeignKey('MCQuestion', on_delete=models.CASCADE,
                                 related_name='choices',
                                 related_query_name='choice')

    class Meta:
        ordering = ['weight']

    @property
    def value(self):
        return self.linked_value.value


class MCQuestion(BaseConcreteQuestion):
    question_form = 'MC'
    num_choices = models.PositiveSmallIntegerField(default=4)

    def check_answer(self, client_answer):
        try:
            correct_answer = self.choices.filter(
                weight=MCChoice.WeightType.CORRECT).get().value
        except MCChoice.DoesNotExist:
            logger.critical(f'{repr(self)} no correct answer, delete self')
            self.delete()
            raise ValidationError('no correct answer')
        return correct_answer == client_answer, correct_answer

    def _render(self, show_all_options=False):
        weights = np.array(self.choices.values_list('weight', flat=True))
        total_cnt = len(weights)
        if total_cnt < self.num_choices:
            raise ValidationError(f"there are {total_cnt} choices, "
                                  f"fewer than {self.num_choices}")

        if show_all_options:
            num_choices = total_cnt
        else:
            num_choices = self.num_choices

        answer_cnt = total_cnt - np.count_nonzero(weights)
        if answer_cnt != 1:
            raise ValidationError(f"there are {answer_cnt} correct answers, "
                                  f"not one")

        choice_indexes = np.random.choice(np.arange(total_cnt),
                                          size=num_choices - 1,
                                          replace=False,
                                          p=weights / np.sum(weights)
                                          ).tolist()
        answer = np.random.randint(num_choices)
        choice_indexes.insert(answer, 0)

        choice_list = list(self.choices.all())
        choices = [choice_list[i].value for i in choice_indexes]
        d = {
            'choices': [choice for choice in choices
                        if choice is not None]
        }
        if self.question_type == 'Pinyin2DefMC':
            d['question'] = {
                'text': self.question,
                'audio': self.reviewable.word.audio_url,
            }
        return d


class FITBQuestion(BaseConcreteQuestion):
    question_form = 'FITB'
    title_link = models.ForeignKey(LinkedField,
                                   on_delete=models.CASCADE,
                                   related_name='+')
    answer_link = models.ForeignKey(LinkedField,
                                    on_delete=models.CASCADE,
                                    related_name='+')
    alternative_answers = ArrayField(
        models.CharField(max_length=8), default=list, blank=True,
        help_text="punctuations and spaces will be ignored, case insensitive"
    )

    def _render(self, show_all_options=False):
        title = self.title_link.value
        answer = self.answer_link.value
        if not answer or not title:
            raise ValidationError("answer or extra_information None")
        return {
            'title': title,
        }

    def clean(self):
        super().clean()
        self.alternative_answers = [self._normalize_answer(answer)
                                    for answer in self.alternative_answers]

    @staticmethod
    def _normalize_answer(x):
        # remove all punctuations and spaces
        return re.sub(
            r'[^a-zA-Z0-9\u2E80-\u2FD5\u3190-\u319f\u3400-\u4DBF'
                r'\u4E00-\u9FCC\uF900-\uFAAD\U00020000-\U0002A6D6]',
            r'',
            x
        ).lower()

    def check_answer(self, client_answer):
        correct_answer = self.answer_link.value
        try:
            client_answer = client_answer.strip()
        except AttributeError:
            logging.error('client answer not string', exc_info=True)
        client_answer = self._normalize_answer(client_answer)
        correct_answers = [
            self._normalize_answer(correct_answer),
            # for words like (飞)机场, allow both 飞机场 and 机场
            self._normalize_answer(re.sub(r'\((.*?)\)', r'', correct_answer)),
            *self.alternative_answers
        ]
        return client_answer in correct_answers, correct_answer


class CNDQuestion(BaseConcreteQuestion):
    question_form = 'CND'
    description = models.TextField(max_length=200, blank=True)
    title_link = models.ForeignKey(LinkedField,
                                   on_delete=models.CASCADE,
                                   related_name='+')
    correct_answers = ArrayField(models.CharField(max_length=5))
    wrong_answers = ArrayField(models.CharField(max_length=5))
    choice_num = models.PositiveSmallIntegerField(default=5)

    def _render(self, show_all_options=False):
        title = self.title_link.value
        if not self.correct_answers:
            raise ValidationError("no correct_answers")
        choices = self.correct_answers.copy()
        if show_all_options:
            wrong_answers = self.wrong_answers
        else:
            wrong_answer_len = max(0, self.choice_num - len(choices))
            wrong_answers = self.wrong_answers[:wrong_answer_len]
        choices.extend(wrong_answers)
        np.random.shuffle(choices)
        return {
            'title': title,
            'description': self.description,
            'answer_length': len(self.correct_answers),
            'choices': choices
        }

    def check_answer(self, client_answer):
        correct_answer = self.correct_answers
        return correct_answer == client_answer, correct_answer
