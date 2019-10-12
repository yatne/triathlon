from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from rest_framework.authtoken.models import Token


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user realization based on Django AbstractUser and PermissionMixin.
    """
    email = models.EmailField(
        ('email address'),
        unique=True,
        error_messages={
            'unique': ("A user with that email already exists."),
        })

    date_joined = models.DateTimeField(('date joined'), default=timezone.now)

    first_name = models.CharField(('first name'), max_length=30)
    last_name = models.CharField(('last name'), max_length=50)

    username = models.CharField(
        ('username'),
        max_length=100,
        unique=True,
        help_text=('Required. 30 characters or fewer. Letters, digits and '
                   '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                ('Enter a valid username. '
                 'This value may contain only letters, numbers '
                 'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': ("A user with that username already exists."),
        })

    facebook_id = models.CharField(max_length=200, unique=True)
    profile_image = models.CharField(max_length=300, default='')
    objects = UserManager()

    # this is needed to use this model with django auth as a custom user class
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        managed = True
        abstract = False
        db_table = 'auth_user'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    Token.objects.get_or_create(user=instance)
