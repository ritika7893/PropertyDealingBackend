from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class RegistrationManager(BaseUserManager):

    def create_user(self, mobile_number, name, password=None, role="user"):

        if not mobile_number:
            raise ValueError("Users must have a mobile number")

        user = self.model(
            mobile_number=mobile_number,
            name=name,
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, mobile_number, name, password):

        user = self.create_user(
            mobile_number=mobile_number,
            name=name,
            password=password,
            role="admin"
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Registration(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )

    user_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    name = models.CharField(max_length=100)

    mobile_number = models.CharField(
        max_length=15,
        unique=True
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="user"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = RegistrationManager()

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = ["name"]

    def save(self, *args, **kwargs):

        if not self.user_id:

            last_user = Registration.objects.order_by("id").last()

            if last_user and last_user.user_id:
                try:
                    last_id = int(last_user.user_id.split("-")[1])
                except (IndexError, ValueError):
                    last_id = 0

                new_id = last_id + 1
            else:
                new_id = 1

            self.user_id = f"USER-{new_id:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name