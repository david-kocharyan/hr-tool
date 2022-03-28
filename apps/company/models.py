from django.db import models

from apps.core.models import TimeStampedAbstractModel
from apps.users.models import User


class Company(TimeStampedAbstractModel):
    owner = models.ForeignKey(User, verbose_name="Owner", related_name='owner', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Name', max_length=50)
    slug = models.SlugField(unique=True)
    industry = models.CharField(verbose_name='Industry', max_length=50)
    description = models.TextField(verbose_name='Description', max_length=500)
    address = models.CharField(verbose_name='Address', max_length=50)
    contacts = models.CharField(verbose_name='Contacts', max_length=50)
    members = models.ManyToManyField(User, verbose_name="Members", related_name='member')

    def __str__(self):
        return self.name
