from django.contrib import admin
from .models import Post ,PostsComment,  PostViews
# Register your models here.


admin.site.register(Post)
admin.site.register(PostViews)
admin.site.register(PostsComment)