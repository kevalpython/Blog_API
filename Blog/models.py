from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
# from django.contrib.auth.models import User

class BaseModel(models.Model):
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

class User(AbstractUser):
    biography = models.CharField(max_length = 255, blank=True, null=True)
    is_blogger = models.BooleanField(default=False)

    def __str__(self):
            return self.username

class Blogs(BaseModel):
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/blog/{self.id}/"

class Comments(BaseModel):
    comment= models.CharField(max_length=255,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE,related_name='comments')

    
    def __str__(self):
        return self.comment