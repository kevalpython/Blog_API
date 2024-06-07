
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Blogs,User,Comments

class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Blogs
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Comments
        exclude = ('user',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


