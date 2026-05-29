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

class Property(models.Model):

    PROPERTY_TYPE_CHOICES = [
        ("villa", "Villa"),
        ("penthouse", "Penthouse"),
        ("house", "House"),
        ("loft", "Loft"),
        ("estate", "Estate"),
        ("home", "Home"),
        ("townhouse", "Townhouse"),
        ("apartment", "Apartment"),
    ]

    STATUS_CHOICES = [
        ("for_sale", "For Sale"),
        ("for_rent", "For Rent"),
        ("sold", "Sold"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    location = models.CharField(max_length=255)

    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)

    area_sqft = models.PositiveIntegerField()

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="for_sale"
    )

    featured_image = models.ImageField(
        upload_to="properties/",blank=True,null=True
    )

    amenities = models.JSONField(default=list)

    year_built = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    listing_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title