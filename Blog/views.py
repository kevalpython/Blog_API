from django.shortcuts import render
from rest_framework.response import Response
from .models import Blogs,User,Comments
from .serializers import BlogsSerializer,CommentSerializer,UserSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView


class BlogsViewSet(viewsets.ViewSet):
    
    def list(self,request):
        blog = Blogs.objects.all()
        blog_serializer = BlogsSerializer(blog, many = True)
        return Response(blog_serializer.data)
    
    def retrieve(self, request,pk=None):
        try:
            blog = Blogs.objects.get(pk=pk)
        except Blogs.DoesNotExist:
            return Response({'error': 'Blog does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        blog_serializer = BlogsSerializer(blog)
        comments = Comments.objects.filter(blog=blog)
        comments_serializer = CommentSerializer(comments, many=True)

        return Response({'blog': blog_serializer.data, 'comments': comments_serializer.data})

class BloggersViewset(viewsets.ViewSet):
    
    def list(self,request):
        user = User.objects.filter(is_blogger=True)
        user_serializer = UserSerializer(user, many = True)
        return Response(user_serializer.data)
    
    def retrieve(self, request,pk=None):
        try:
            user = User.objects.get(pk=pk)
        except Blogs.DoesNotExist:
            return Response({'error': 'Blog does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        user_serializer = UserSerializer(user)
        return Response({'blog': user_serializer.data})
    


class AddCommentViewset(viewsets.ViewSet):
    def create(self, request):
        serializer = CommentSerializer(data=request.data)
        print("serializer ===========> ",serializer)
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
