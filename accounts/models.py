from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class DisplayNameValidator(validators.RegexValidator):
    regex = r"^[\w\d\u2E80-\u2FD5\u3190-\u319f\u3400-\u4DBF\u4E00-\u9FCC\uF900-\uFAAD]+" \
            r"[\ \-\w\d\u2E80-\u2FD5\u3190-\u319f\u3400-\u4DBF\u4E00-\u9FCC\uF900-\uFAAD]*?" \
            r"[\w\d\u2E80-\u2FD5\u3190-\u319f\u3400-\u4DBF\u4E00-\u9FCC\uF900-\uFAAD]+$"
    message = _(
        'Enter a valid display name. This value may contain only letters, '
        'Chinese characters, numbers, and space/-. Space/- may appear'
        ' only in the middle. Minimum length is 2. '
    )


class User(AbstractUser):
    display_name = models.CharField(max_length=30, blank=True,
            validators=[DisplayNameValidator()],
            help_text="This is the name displayed to others. We recommend using"
                      " your real name. Leave blank to use your username. "
                      "You may change this later.")
    email = models.EmailField(
        help_text="Used for resetting your password and receiving notifications. "
                  "This could also be used for login.",
        null=True, blank=True, unique=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    class Meta:
        ordering = ('-last_login',)

    def clean(self):
        if self.email == '':
            self.email = None
        super().clean()

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.display_name} ({self.username})"

    def __repr__(self):
        return f"<user {self.pk}: {self.display_name} ({self.username})>"
