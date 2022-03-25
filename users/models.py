from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid

from users.managers import UserManager


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        TEACHER = "Teacher"
        STUDENT = "Student"

    """Custom user model"""
    username = None
    email = models.EmailField("Email", unique=True)
    first_name = models.CharField("First name", max_length=150)
    last_name = models.CharField("Last name", max_length=150)
    role = models.CharField("Role", max_length=7, choices=RoleChoices.choices)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}({self.role})"
