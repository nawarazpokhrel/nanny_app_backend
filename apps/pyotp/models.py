import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class PyOTP(models.Model):
    """
    PyOTP Model
    """
    PURPOSE_CHOICES = (
        ('R', 'PasswordReset'),
        ('A', 'Activation'),
        ('P', 'PhoneNumberVerification'),
        ('E', 'EmailVerification'),
        ('2FA', 'TwoFactorAuthentication'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    secret = models.CharField(
        _('Secret'),
        null=False,
        blank=False,
        max_length=50,
        help_text=_('Secret used to generate OTP.'),
    )
    interval = models.IntegerField(
        _('Interval (in seconds)'),
        null=True,
        blank=True,
        help_text=_('OTP Count, to be used in case of TOTP.'),
    )
    otp = models.CharField(
        _('OTP'),
        null=False,
        blank=False,
        max_length=10,
        help_text=_('Generated OTP.'),
    )
    purpose = models.CharField(
        _('Purpose'),
        null=False,
        blank=False,
        choices=PURPOSE_CHOICES,
        max_length=3,
        help_text=_('Purpose of OTP.'),
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        db_index=True,
    )
    expires_at = models.DateTimeField(
        _('expires at'),
        db_index=True,
    )

    # Meta
    class Meta:
        default_permissions = ()
        verbose_name = _("PyOtp")
        verbose_name_plural = _("PyOtp")

    # Functions
    def __str__(self):
        return str(self.user)

