from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('Blogs', views.BlogsViewSet, basename='Blogs')
router.register('Bloggers', views.BloggersViewset,  basename='Bloggers')
router.register('AddComment', views.AddCommentViewset,  basename='AddComment')

urlpatterns = [
    path("", include(router.urls)),
    path ("auth/", include('rest_framework.urls', namespace='rest_framework')),
]