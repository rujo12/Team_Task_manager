"""
User serializers.

Serializers for user signup, login, and profile operations.
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
import re

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for user profiles."""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role", "full_name", "date_joined")
        read_only_fields = ("id", "role", "date_joined")
    
    def get_full_name(self, obj):
        """Get user's full name or username as fallback."""
        return obj.get_full_name()


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup/registration.
    
    Validates:
    - Username: 3-30 chars, alphanumeric + underscore, unique
    - Email: valid format, unique
    - Password: min 8 chars, contains letters and numbers, matches confirmation
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Password must be at least 8 characters including letters and numbers"
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=False,
        style={"input_type": "password"},
        help_text="Re-enter password for confirmation"
    )
    # Backward-compatible alias for older payloads.
    password_confirm = serializers.CharField(
        write_only=True,
        required=False,
        style={"input_type": "password"},
        help_text="Backward-compatible password confirmation field"
    )
    
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "confirm_password",
            "password_confirm",
            "first_name",
            "last_name",
            "role",
        )
        read_only_fields = ("id",)
        extra_kwargs = {
            "first_name": {"required": False, "allow_blank": True},
            "last_name": {"required": False, "allow_blank": True},
            "email": {"required": True},
            "role": {"required": False},
        }
    
    def validate_username(self, value):
        """
        Validate username format and uniqueness.
        
        Requirements:
        - 3-30 characters
        - Alphanumeric + underscore only
        - Must start with letter
        - Unique
        """
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters long."
            )
        
        if len(value) > 30:
            raise serializers.ValidationError(
                "Username must be no longer than 30 characters."
            )
        
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", value):
            raise serializers.ValidationError(
                "Username must start with a letter and contain only letters, numbers, and underscores."
            )
        
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already taken."
            )
        
        return value
    
    def validate_email(self, value):
        """
        Validate email uniqueness.
        
        Email must be unique if provided.
        """
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )
        
        return value
    
    def validate_password(self, value):
        """
        Validate password strength.
        
        Requirements:
        - At least 8 characters
        - Contains at least one letter
        - Contains at least one number
        - Passes Django's built-in validators
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one letter."
            )
        
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )
        
        # Use Django's built-in password validators
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        
        return value
    
    def validate(self, attrs):
        """
        Validate that password and confirmation field match.
        """
        password = attrs.get("password")
        confirm_password = attrs.pop("confirm_password", None)
        legacy_password_confirm = attrs.pop("password_confirm", None)
        confirmed_value = confirm_password or legacy_password_confirm

        if password and confirmed_value is None:
            raise serializers.ValidationError({
                "confirm_password": "This field is required."
            })

        if password and confirmed_value != password:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })
        
        return attrs
    
    def create(self, validated_data):
        """
        Create a new user with hashed password.
        
        Uses create_user() which:
        - Hashes the password securely
        - Sets other fields properly
        - Returns the created user
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            role=validated_data.get("role", "MEMBER"),
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login requests (for documentation)."""
    
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that includes additional user info in response.
    
    Adds custom claims to the token and returns user data with tokens.
    """
    
    @classmethod
    def get_token(cls, user):
        """
        Add custom claims to JWT token.
        
        Custom claims:
        - email: User email
        - username: User username
        - first_name: User first name
        - last_name: User last name
        """
        token = super().get_token(user)
        
        # Add custom claims
        token["email"] = user.email
        token["username"] = user.username
        token["user_id"] = str(user.id)
        
        return token
    
    def validate(self, attrs):
        """
        Validate login credentials and add user info to response.
        """
        data = super().validate(attrs)
        
        # Add user info to response for convenience
        data["user"] = UserSerializer(self.user).data
        
        return data
