from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.user.manager import UserManager


# Create your models here.
class Role(models.TextChoices):
    ADMIN = 'admin', _('Admin')
    MANAGER = 'manager', _('Manager')
    USER = 'user', _('User')


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True
    )
    phone_number = PhoneNumberField(
        null=True, blank=True,
    )
    full_name = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'



class RefreshToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='refresh_tokens'
    )
    token = models.CharField(
        max_length=255,
        unique=True
    )
    used_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"Token: {self.token[:20]}..."

    class Meta:
        verbose_name = 'Refresh Token'
        verbose_name_plural = 'Refresh Tokens'
