from django.db import models

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Permission, Group

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin, BaseUserManager, Permission

from apps.core.models import TimeStampedAbstractModel

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'email': 'email'}


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email or not password:
            raise ValueError('User must have an email address and password')

        email = email.lower()
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        email = email.lower()
        user = self.create_user(email, password=password)
        user.is_staff, user.is_superuser, user.is_active = True, True, True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedAbstractModel):
    email = models.EmailField(verbose_name='Email Address', unique=True)
    password = models.CharField(verbose_name='Password', max_length=125, null=True)
    first_name = models.CharField(verbose_name='First Name', max_length=125, null=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=125, null=True)
    dob = models.DateField(verbose_name='Date of Birth', null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))

    active_company = models.ForeignKey("company.Company", verbose_name="Active Company", on_delete=models.CASCADE,
                                       null=True)

    # permissions = models.ManyToManyField(Permission)
    # groups = models.ManyToManyField(Group)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __str__(self):
        return self.email


class ForgetPassword(TimeStampedAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True)

    def __str__(self):
        return self.user
