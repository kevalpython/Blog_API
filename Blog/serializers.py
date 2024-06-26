"""
This module contains serializer for passing data into json format.
"""

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Blogs, Comments, User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class BlogsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Blogs model.
    """

    class Meta:
        """
        Metadata options for the BlogsSerializer.
        """

        model = Blogs
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comments model.
    """

    class Meta:
        """
        Metadata options for the CommentSerializer.
        """

        model = Comments
        exclude = ("user",)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        """
        Metadata options for the UserSerializer.
        """

        model = User
        fields = "__all__"
        
        
class UserActivationSerializer(serializers.ModelSerializer):
    """
    Serializer for the User Activation model.
    """

    class Meta:
        """
        Metadata options for the UserSerializer.
        """

        model = User
        fields = ["id", "username","is_active"]