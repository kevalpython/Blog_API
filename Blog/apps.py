"""
This module configures the app within the main project folder.
"""

from django.apps import AppConfig


class BlogsConfig(AppConfig):
    """
    This module handles the configuration of the app within the main project folder.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "Blog"
