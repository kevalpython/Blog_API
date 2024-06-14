"""
This module contains views for passing data to the frontend or user.
"""

from rest_framework import permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Blogs, Comments, User
from .serializers import BlogsSerializer, CommentSerializer, UserSerializer


class BlogsViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling CRUD operations related to blogs.

    Attributes:
        None
    """

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

    def retrieve(self, pk=None):
        """
        Retrieve a single blog with its associated comments.

        Args:
            request: The request object.
            pk (int): The primary key of the blog.

        Returns:
            Response: A serialized blog along with its comments.
        """
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


class BloggersViewset(viewsets.ViewSet):
    """
    A ViewSet for handling CRUD operations related to bloggers.

    Attributes:
        None
    """

    def list(self):
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

    def retrieve(self, pk=None):
        """
        Retrieve a single blogger.

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
