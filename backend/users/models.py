"""
User model for Team Task Manager.

Custom User model extending Django's AbstractUser for future extensibility.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    Inherits from AbstractUser:
        - id, username, password, first_name, last_name
        - is_active, is_staff, is_superuser
        - date_joined, last_login
    
    Overrides:
        - email: Optional to prevent createsuperuser from asking for it
    
    USERNAME_FIELD = 'username' (inherited from AbstractUser)
    REQUIRED_FIELDS = [] (prevents email/other fields from being asked during createsuperuser)
    """
    
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("MEMBER", "Member"),
    ]

    email = models.EmailField(
        unique=True,
        blank=True,  # Make optional so createsuperuser doesn't ask for it
        validators=[EmailValidator()],
        help_text="User's email address (optional, but unique if provided)"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="MEMBER",
        help_text="Global role used for API access control."
    )
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
        ]
    
    # REQUIRED_FIELDS determines which fields are prompted during createsuperuser
    # By default, AbstractUser sets REQUIRED_FIELDS = ['email']
    # We override to empty list to prevent email prompt during createsuperuser
    # USERNAME_FIELD (username) is always required, doesn't need to be here
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email if self.email else self.username
    
    def get_full_name(self):
        """Return the first and last name."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username
