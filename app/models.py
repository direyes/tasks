from django.db import models
from django.utils.translation import ugettext as _


class Task(models.Model):
    """model to task"""

    description = models.CharField(
        max_length=240,
        verbose_name=_('description'),
    )
    complete = models.BooleanField(
        default=False,
        verbose_name=_('complete'),
    )
    owner = models.ForeignKey(
        'auth.User',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_('owner'),
    )
