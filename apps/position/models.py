from django.db import models

from apps.company.models import Company
from apps.core.models import TimeStampedAbstractModel
from django.contrib.postgres.fields import ArrayField


class Position(TimeStampedAbstractModel):
    company = models.ForeignKey(Company, verbose_name="Company", on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Name', max_length=50)
    description = models.TextField(verbose_name='Description', max_length=500)
    skill = ArrayField(models.CharField(max_length=50, null=True), verbose_name="Skills")
    number = models.PositiveSmallIntegerField(verbose_name='Number')

    def __str__(self):
        return self.name
