from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator, EmailValidator

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

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[EmailValidator(message="Enter a valid email address with @.com format")])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Common fields for both types of users
    user_type = models.CharField(max_length=10, choices=[('student', 'Student'), ('admin', 'Admin')])

    # Student specific fields
    student_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=10, null=True, blank=True)

    # Admin specific fields
    admin_id = models.IntegerField(null=True, blank=True)
    admin_role = models.CharField(
        max_length=20, 
        choices=[
            ('hostel', 'Hostel Admin'),
            ('infra', 'Infrastructure Admin'),
            ('exam', 'Examination Admin')
        ],
        null=True, 
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.user_type == 'student':
            return f"Student: {self.email} ({self.student_id if self.student_id else 'No ID'})"
        elif self.user_type == 'admin':
            return f"Admin: {self.email} - {self.get_admin_role_display()}"
        return f"User: {self.email}"
