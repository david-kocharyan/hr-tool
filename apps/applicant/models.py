from django.db import models

from apps.company.models import Company
from apps.core.models import TimeStampedAbstractModel
from django.contrib.postgres.fields import ArrayField

from apps.position.models import Position

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)
LEVEL = (
    ("junior", "Junior"),
    ("middle", "Middle"),
    ("senior", "Senior"),
    ("team_lead", "Team lead"),
)
STATUS = (
    ("shortlisted", "Shortlisted"),
    ("not_considered", "Not considered"),
    ("interviewing", "Interviewing"),
    ("rejected", "Rejected"),
    ("for_future_consideration", "For future consideration"),
    ("black_list", "Black list"),
)


class Apllicant(TimeStampedAbstractModel):
    company = models.ForeignKey(Company, verbose_name="Company", on_delete=models.CASCADE)
    position_applied = models.ForeignKey(Position, verbose_name='Position', null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(verbose_name='First name', max_length=50)
    last_name = models.CharField(verbose_name='Last name', max_length=50)
    email = models.EmailField(verbose_name='Email', max_length=125)
    phone = models.CharField(verbose_name='Phone', max_length=30)
    gender = models.CharField(verbose_name='Gender', max_length=20, choices=GENDER, default='male')
    country = models.TextField(verbose_name='Country', max_length=50)
    dob = models.DateField(verbose_name='Date of Birth')
    level = models.TextField(verbose_name='Level', max_length=50, choices=LEVEL, default='junior')
    skill = ArrayField(models.CharField(max_length=50, null=True), verbose_name="Skills")
    comment = models.TextField(verbose_name='Comment', max_length=500)
    status = models.TextField(verbose_name='Status', max_length=60, choices=STATUS, default='shortlisted')
    cv = models.FileField(verbose_name='CV')

    def __str__(self):
        return self.name
