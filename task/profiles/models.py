from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, fio, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(fio=fio, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, fio, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(fio, email, password, **extra_fields)

    def create_superuser(self, fio, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(fio, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    fio = models.CharField(max_length=120)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default=None)
    role = models.CharField(max_length=50, blank=True)
    current_projects = models.ManyToManyField('Project', blank=True, related_name='profiles_current_users')
    project_history = models.ManyToManyField('Project', blank=True, related_name='profiles_historical_users')

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='profiles_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='profiles_user_set',
        related_query_name='user',
    )

    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = ['fio', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
