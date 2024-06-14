"""
This module contains Django model definitions.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with common fields for other models.
    """

    class Meta:
        """
        Metadata options for the CommentSerializer.
        """

        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)


class User(AbstractUser):
    """
    Custom user model with additional fields.
    """

    biography = models.CharField(max_length=255, blank=True, null=True)
    is_blogger = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of a user.
        """
        return str(self.username)


class Blogs(BaseModel):
    """
    Model for blog posts.
    """

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        String representation of a blog post.
        """
        return str(self.title)

    def get_absolute_url(self):
        """
        Returns the absolute URL of the blog post.
        """
        return f"/blog/{self.id}/"


class Comments(BaseModel):
    """
    Model for comments on blog posts.
    """

    comment = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        """
        String representation of a comment.
        """
        return str(self.comment)
