from rest_framework.pagination import PageNumberPagination
from .models import Blogs,User,Comments
from .serializers import BlogsSerializer,CommentSerializer,UserSerializer
from rest_framework import viewsets, permissions,status
from rest_framework.response import Response


class BlogsViewSet(viewsets.ViewSet):

    def list(self, request):
        blog = Blogs.objects.all()
        paginator = PageNumberPagination()  
        paginator.page_size = 2  
        paginated_comments = paginator.paginate_queryset(blog, request)
        blog_serializer = BlogsSerializer(paginated_comments, many=True)
        return paginator.get_paginated_response(blog_serializer.data)
    
    def retrieve(self, request, pk=None):
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

    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request):
        serializer = CommentSerializer(data=request.data)
        print("serializer ===========> ",serializer)
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

