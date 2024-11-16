from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

User = get_user_model()

from blog.views import (  
    PostsListsViews,  PostsDetailViews, DeletePostComment,  
    EditPostComment,  CretePost,  UpdatePost,  DeletePost, 
)

from blog.models import Post

class TestBlogViewAndUrl(TestCase):

    def setUp(self):
        
        # create user as author
        user = User.objects.create_user(
            email = 'post@post.com',
            password = '1234'
        )

        user.is_verified = True
        user.save()

        # create a post and test it here
        post  = Post.objects.create(
            title = 'test',
            author= user,
            text = 'test'    
        )

        # get the post and check 
        post = Post.objects.filter(title='test', id=post.id).exists()
        self.assertTrue(post)
        

    def test_post_list_view_with_get_view_and_url(self):
        
        url = reverse('PostsListsViews')
        client = Client()

        # check the url and view
        self.assertEqual(resolve(url).func.view_class, PostsListsViews)        

        # send request
        response = client.get(url)

        # check with get method
        self.assertEqual(response.status_code, 200)

    
    def test_post_detail_view_with_get_method_and_url(self):

        # get any post object
        post = Post.objects.all()[0]

        # get the client and url
        url = reverse('PostsDetailViews', kwargs={'pk': post.id})
        client = Client()

        pass 