from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .user_manager import UserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from django.core.validators import RegexValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True) # changes email to unique and blank to false
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    
    phone_regex = RegexValidator(regex=r'^\+\d{7,15}$', message="Phone number must be entered in the format: '+999999999'. [7, 15] digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16, blank=True)


    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []