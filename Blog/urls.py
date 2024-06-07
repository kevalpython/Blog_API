from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView

router = DefaultRouter()

router.register('Blogs', views.BlogsViewSet, basename='Blogs')
router.register('Bloggers', views.BloggersViewset, basename='Bloggers')
router.register('AddComment', views.AddCommentViewset, basename='AddComment')

urlpatterns = [
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("token/verify/", TokenVerifyView.as_view(), name='verify'),
    path("auth/", include('rest_framework.urls', namespace='rest_framework')),
]

