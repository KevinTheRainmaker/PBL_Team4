

from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):
    """Time Stamped Model"""

    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="주문일")
    modifeid_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
