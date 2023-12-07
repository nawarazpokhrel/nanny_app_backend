from datetime import timedelta
import pyotp
from django.conf import settings
from django.utils import timezone

from apps.pyotp.models import PyOTP


class OTPMixin:
    """
        Apply this mixin to Perform Various operations of PyOTP.
    """

    @staticmethod
    def _get_random_base32_string():
        """Generate Random Base32 string
        """
        return pyotp.random_base32()

    @staticmethod
    def _insert_into_db(otp, secret=None, interval=None, user=None, purpose=None):
        """
        :param secret: otp secret.
        :param interval: totp interval
        :return: otp object
        """
        expires_at = timezone.now() + timedelta(seconds=interval)
        fields = {
            'user': user,
            'otp': otp,
            'secret': secret,
            'interval': interval,
            'purpose': purpose,
            'expires_at': expires_at,
        }

        return PyOTP.objects.create(**fields)

    def _generate_totp(self, user, purpose, interval=settings.OTP_INTERVAL):
        """Generates time-based OTPs
        """
        PyOTP.objects.filter(user=user, purpose=purpose).delete()

        base32string = self._get_random_base32_string()
        totp = pyotp.TOTP(base32string, interval=interval)
        otp = totp.now()

        # save data into db
        self._insert_into_db(otp, secret=base32string, interval=interval, user=user, purpose=purpose)
        return otp

    def _regenerate_totp(self, user, purpose, interval=settings.OTP_INTERVAL):
        """Generates time-based OTPs
        """
        try:
            otp = PyOTP.objects.get(
                user=user,
                purpose=purpose,
                expires_at__gt=timezone.now(),
            )
        except PyOTP.DoesNotExist:
            return self._generate_totp(
                user=user,
                purpose=purpose,
                interval=interval
            )

        return otp.otp

    @staticmethod
    def verify_otp(otp, obj):
        """
        :param obj:
        :param otp:
        :return:
        """
        if obj.interval:
            totp = pyotp.TOTP(obj.secret, interval=obj.interval)
            is_valid = totp.verify(otp)
            if is_valid:
                obj.delete()
            return is_valid
        return False

    @staticmethod
    def verify_otp_for_user(user, otp, purpose):
        """
        :param purpose:
        :param otp:
        :return:
        """
        try:
            obj = PyOTP.objects.get(
                user=user,
                otp=otp,
                purpose=purpose,
                expires_at__gt=timezone.now()
            )
        except PyOTP.DoesNotExist:
            return False
        obj.delete()
        return True
