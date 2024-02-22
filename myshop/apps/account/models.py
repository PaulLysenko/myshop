import uuid

import pyotp
import qrcode
import qrcode.image.svg

from django.db import models
from django.contrib.auth.models import User


class RegTry(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    otc = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    c_time = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.email} at {self.c_time.strftime('%d-%m-%Y %H:%M:%S')}"


class Profile(models.Model):
    # make data migration - create profiles for all users without profiles
    # user creation - create profile for user
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    api_key = models.UUIDField(default=uuid.uuid4, db_index=True)


class UserTwoFactorAuthData(models.Model):
    user = models.OneToOneField(
        User,
        related_name='two_factor_auth',
        on_delete=models.CASCADE
    )

    gauth_secret = models.CharField(max_length=32, editable=False, default=pyotp.random_base32)

    def generate_qr_code(self, name=None) -> str:
        totp = pyotp.TOTP(self.gauth_secret)
        qr_uri = totp.provisioning_uri(
            name=name,
            issuer_name='2FA Gauth for MyShop',
        )

        image_factory = qrcode.image.svg.SvgPathImage
        qr_code_image = qrcode.make(
            qr_uri,
            image_factory=image_factory,
        )

        # The result is going to be an HTML <svg> tag
        return qr_code_image.to_string().decode('utf_8')

    def validate_otp(self, otp: str) -> bool:
        totp = pyotp.TOTP(self.gauth_secret)

        return totp.verify(otp)