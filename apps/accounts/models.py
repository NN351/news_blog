from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email=None,password=None, **extra_fields):
        if not email:
            raise ValueError("Email is must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    email = models.EmailField("Электронная почта", unique=True)
    image = models.ImageField("Аватарка",  upload_to="user/images/")
    is_verified = models.BooleanField("Верифицирован",  default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    
    def __str__(self):
        return f"{self.email}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    




# Термины: 
# Хеширование - Односторонная функция , полученный результат нельзя обратит назад 
# и получить исходное значение.

# qwerty123 --- > ХЕШИРОВАНИЕ ----> skladfjlasj10851pjflkdjsflkjwepju315kj

# qwerty123 ----> ХЕШИРОВАНИЕ ----> skladfjlasj10851pjflkdjsflkjwepju315kj == skladfjlasj10851pjflkdjsflkjwepju315kj



# 2)
# Шифрование - двухсторонная функция, полученный шифр можно с помощью ключа расшифровать
# Hello World ---> Шифрование(Ключ) --> sdlkfjlkj23512lj12;5k12pk5sadf ---> Дешифрование(Ключ) ----> Hello World