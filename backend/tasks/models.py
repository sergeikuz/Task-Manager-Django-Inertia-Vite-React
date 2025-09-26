from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.labels.models import Label
from backend.statuses.models import Status
from backend.users.models import User


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name=_("Status")
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="tasks_owned",
        verbose_name=_("Owner")
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="tasks_executed",
        verbose_name=_("Executor")
    )
    labels = models.ManyToManyField(
        Label,
        related_name="tasks_labels",
        verbose_name=_("Labels"),
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"))
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"))

    def __str__(self):
        return self.name
