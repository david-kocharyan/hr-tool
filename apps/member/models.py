from django.db import models

from apps.core.models import TimeStampedAbstractModel
from apps.company.models import Company


class Invite(TimeStampedAbstractModel):
    company = models.ForeignKey(Company, verbose_name="Company", on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='Email')
    uuid = models.UUIDField(unique=True)

    def __str__(self):
        return self.email
