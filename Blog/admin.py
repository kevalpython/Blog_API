from django.contrib import admin
from Blog.models import *

# Register your models here.

@admin.register(User)
class User_Admin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'email', 'biography', 'is_blogger']

class Blog_Comments_Inline(admin.TabularInline):
    model = Comments
    extra = 0

@admin.register(Blogs)
class Blogs_Admin(admin.ModelAdmin):
    list_display = ['title', 'descriptions', 'author', 'created_at', 'updated_at']
    def descriptions(self, obj):
        if len(obj.description) > 75:
            return obj.description[:75] + '...'
        else :
            return obj.description
    inlines = [Blog_Comments_Inline]

@admin.register(Comments)
class Comments_Admin(admin.ModelAdmin):
    list_display = ['comments', 'user', 'blog', 'created_at', 'updated_at']

    def comments(self, obj):
        if len(obj.comment) > 75:
            return obj.comment[:75] + '...'
        else:
            return obj.comment