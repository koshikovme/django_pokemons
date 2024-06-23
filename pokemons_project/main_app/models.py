from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# Определение типов покемонов
class PokemonType(models.TextChoices):
    NORMAL = 'NO', _('Normal')
    FIRE = 'FI', _('Fire')
    WATER = 'WA', _('Water')
    GRASS = 'GR', _('Grass')
    ELECTRIC = 'EL', _('Electric')
    ICE = 'IC', _('Ice')
    FIGHTING = 'FI', _('Fighting')
    POISON = 'PO', _('Poison')
    GROUND = 'GR', _('Ground')
    FLYING = 'FL', _('Flying')
    PSYCHIC = 'PS', _('Psychic')
    BUG = 'BU', _('Bug')
    ROCK = 'RO', _('Rock')
    GHOST = 'GH', _('Ghost')
    DRAGON = 'DR', _('Dragon')
    DARK = 'DA', _('Dark')
    STEEL = 'ST', _('Steel')
    FAIRY = 'FA', _('Fairy')

# Модель Атаки
class Attack(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=2,
        choices=PokemonType.choices,
        default=PokemonType.NORMAL,
    )
    power = models.PositiveIntegerField()
    accuracy = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# Модель Покемона
class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    type1 = models.CharField(
        max_length=2,
        choices=PokemonType.choices,
        default=PokemonType.NORMAL,
    )
    type2 = models.CharField(
        max_length=2,
        choices=PokemonType.choices,
        blank=True,
        null=True
    )
    level = models.PositiveIntegerField(default=1)
    hp = models.PositiveIntegerField()
    attack = models.PositiveIntegerField()
    defense = models.PositiveIntegerField()
    special_attack = models.PositiveIntegerField()
    special_defense = models.PositiveIntegerField()
    speed = models.PositiveIntegerField()
    attacks = models.ManyToManyField(Attack, related_name='pokemons')

    def __str__(self):
        return self.name

# Модель Тренера
class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    pokemons = models.ManyToManyField(Pokemon, related_name='users')

    login = models.CharField(max_length=100)
    password = models.CharField(max_length=)

    def __str__(self):
        return self.name
