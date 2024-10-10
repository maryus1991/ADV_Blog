from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """
    the posts models
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image  = models.ImageField(upload_to='posts', null=True, blank=True)
    image2  = models.ImageField(upload_to='posts', null=True, blank=True)

    title = models.CharField(max_length=255)
    text = models.TextField()
    text2 = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class PostViews(models.Model):
    """
    for counting views for posts
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='view')
    ip = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.post.title}'
    

class PostsComment(models.Model):
    """
    post comment models 
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name + '/' + self.email

    
