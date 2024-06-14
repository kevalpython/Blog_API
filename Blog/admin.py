"""
This module contains admin panels for managing the Blogs app.
"""

from django.contrib import admin

from Blog.models import Blogs, Comments, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    This class displays user data in the admin panel.
    """

    list_display = ["username", "first_name", "email", "biography", "is_blogger"]


class BlogCommentsInline(admin.TabularInline):
    """
    This class displays comments in tabular form in the admin panel.
    """

    model = Comments
    extra = 0


@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    """
    This class displays blogs in the admin panel.
    """

    list_display = ["title", "descriptions", "author", "created_at", "updated_at"]

    def descriptions(self, obj):
        """
        This method displays the description of a blog, limited to 75 characters with "..." if longer, in the admin panel.

        obj : This argument returns all fields declared in the Blogs Model.

        It returns the first 75 characters of the description followed by "..." to the admin panel.
        """
        if len(obj.description) > 75:
            return obj.description[:75] + "..."
        return obj.description

    inlines = [BlogCommentsInline]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """
    This class displays comments in the admin panel.
    """

    list_display = ["comments", "user", "blog", "created_at", "updated_at"]

    def comments(self, obj):
        """
        This method displays comments, limited to 75 characters with "..." if longer, in the admin panel.

        obj : This argument returns all fields declared in the Comments Model.

        It returns the first 75 characters of the comment followed by "..." to the admin panel.
        """
        if len(obj.comment) > 75:
            return obj.comment[:75] + "..."
        return obj.comment
