from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField

# get the user model
User = get_user_model()

class CategoryManager(models.Manager):
    """
    for showing just active objects
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by("-id").all()

class Category(models.Model):
    """
    create category model for posts
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, db_index=True)
    is_active = models.BooleanField()

    objects = CategoryManager()

    def __str__(self):
        return f'{self.title} / {self.slug}' 
    

class Post(models.Model):
    """
    the posts models
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="posts", null=True, blank=True)
    image2 = models.ImageField(upload_to="posts", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    text = RichTextUploadingField()
    text2 = RichTextUploadingField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class PostViews(models.Model):
    """
    for counting views for posts
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="view")
    ip = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post.title}"


class PostsCommentsManager(models.Manager):
    """
    for showing just active objects
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by("-id").all()


class PostsComment(models.Model):
    """
    post comment models
    """

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = RichTextUploadingField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", related_name="child", on_delete=models.CASCADE, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = PostsCommentsManager()

    def __str__(self):
        return self.full_name + "/" + self.email
