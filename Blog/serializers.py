"""
This module contains serializer for passing data into json format.
"""

from rest_framework import serializers

from .models import Blogs, Comments, User


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
