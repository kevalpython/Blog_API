"""
This module contains views for passing data to the frontend or user.
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Blogs, Comments, User
from .serializers import (BlogsSerializer, CommentSerializer,
                          RegisterSerializer, UserSerializer)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class BlogsViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling CRUD operations related to blogs.

    Attributes:
        None
    """

    def create(self, request):
        serializer = BlogsSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Data Created", "status": status.HTTP_201_CREATED})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Retrieve a paginated list of blogs.

        Args:
            request: The request object.

        Returns:
            Response: A paginated response containing serialized blogs.
        """
        blog = Blogs.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        paginated_blogs = paginator.paginate_queryset(blog, request)
        blog_serializer = BlogsSerializer(paginated_blogs, many=True)
        return paginator.get_paginated_response(blog_serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a single blog with its associated comments.

        Args:
            request: The request object.
            pk (int): The primary key of the blog.

        Returns:
            Response: A serialized blog along with its comments.
        """
        print(pk)
        try:
            blog = Blogs.objects.get(pk=pk)
        except Blogs.DoesNotExist:
            return Response(
                {"error": "Blog does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        blog_serializer = BlogsSerializer(blog)
        comments = Comments.objects.filter(blog=blog)
        comments_serializer = CommentSerializer(comments, many=True)

        return Response(
            {"blog": blog_serializer.data, "comments": comments_serializer.data}
        )

    def partial_update(self, request, pk=None):
        """
        Partially update a blog if it belongs to the logged-in user.

        Args:
            request: The request object.
            pk (int): The primary key of the blog.

        Returns:
            Response: A response indicating success or failure.
        """
        blog = get_object_or_404(Blogs, pk=pk, author=request.user)
        serializer = BlogsSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        blog = get_object_or_404(Blogs, pk=pk, author=request.user)
        blog.delete()
        return Response({"msg": "Data Deleted", "status": status.HTTP_201_CREATED})


class BloggersViewset(viewsets.ViewSet):
    """
    A ViewSet for handling CRUD operations related to bloggers.
    """

    def list(self, request):
        """
        Retrieve a list of bloggers.

        Args:
            request: The request object.

        Returns:
            Response: A list of serialized bloggers.
        """
        user = User.objects.filter(is_blogger=True)
        user_serializer = UserSerializer(user, many=True)
        return Response(user_serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a single blogger.

        working on Django Rest Framework task
        working singup and login auth views
        working on active blogger and deactive blogger in DRF task
        working crud operation by login user on own blogs


        Args:
            request: The request object.
            pk (int): The primary key of the blogger.

        Returns:
            Response: A serialized blogger.
        """
        try:
            user = User.objects.get(pk=pk)
        except Blogs.DoesNotExist:
            return Response(
                {"error": "Blogger does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        user_serializer = UserSerializer(user)
        return Response({"blogger": user_serializer.data})


class AddCommentViewset(viewsets.ViewSet):
    """
    A ViewSet for adding comments to blogs.

    Attributes:
        permission_classes (list): A list of permission classes required for adding comments.
    """

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        """
        Create a new comment.

        Args:
            request: The request object.

        Returns:
            Response: A serialized comment if creation is successful, else error response.
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
