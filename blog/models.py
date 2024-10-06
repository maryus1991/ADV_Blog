from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image  = models.ImageField(upload_to='posts', null=True, blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title
    

class PostsComment(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.full_name + '/' + self.email

    
