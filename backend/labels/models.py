from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Name"))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"))
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"))
    messege_valid = _("Label is in use and cannot be deleted.")

    def __str__(self):
        return self.name

    def can_delete(self):
        return not self.tasks_labels.exists()

    def delete(self, *args, **kwargs):
        if not self.can_delete():
            raise ValidationError(self.messege_valid)
        super().delete(*args, **kwargs)
        return True
