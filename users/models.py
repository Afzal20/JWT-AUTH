from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('Email Address'), unique=True)
    otp_hash = models.CharField(_('OTP Hash'), max_length=255, blank=True, null=True)
    otp_created_at = models.DateTimeField(_('OTP Created At'), blank=True, null=True)
    is_verified = models.BooleanField(_('Verified'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_otp(self):
        otp = get_random_string(length=6, allowed_chars='0123456789')
        self.otp_hash = make_password(otp)
        self.otp_created_at = datetime.now()
        self.save()
        return otp

    def validate_otp(self, otp):
        if not self.otp_created_at or self.otp_created_at < now() - timedelta(minutes=10):
            return False  # OTP expired
        return check_password(otp, self.otp_hash)

