from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.constants import ITEM_STATUS


class Item(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(max_length=255)
    status = models.CharField(
        max_length=9,
        choices=(
            (ITEM_STATUS.PENDING, _('pending')),
            (ITEM_STATUS.DONE, _('done')),
        )
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, editable=False)
    modified = models.DateTimeField(auto_now=True)
