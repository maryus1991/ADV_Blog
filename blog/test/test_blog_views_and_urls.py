from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

User = get_user_model()

from blog.views import (  
    PostsListsViews,  PostsDetailViews, DeletePostComment,  
    EditPostComment,  CretePost,  UpdatePost,  DeletePost, 
)

from blog.models import Post, PostsComment

class TestBlogViewAndUrl(TestCase):

    def setUp(self):
        
        # create user as author
        self.user = User.objects.create_user(
            email = 'post@post.com',
            password = '1234'
        )
        user = self.user

        user.is_verified = True
        user.save()

        # create a post and test it here
        post  = Post.objects.create(
            title = 'test',
            author= user,
            text = 'test',
            image='media/assets/images/featured/featured/3rd-image.png'    
        )

        
        self.post = post

        client = Client()

        client.login(
            email = 'post@post.com',
            password = '1234'
        )
        self.client = client

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

        # get the client and url and  test the url
        url = reverse('PostsDetailViews', kwargs={'pk': post.id})
        self.assertEqual(resolve(url).func.view_class, PostsDetailViews)
        client = Client()

        # send the request and get the response and test 

        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # test the create comment
        response = client.post(url, data={
            'full_name': 'mez',
            'email': 'test@test.com',
            'comment': 'test test'
        }) 
        self.assertEqual(response.status_code, 302)

        # check the comment in database
        comment = PostsComment.objects.filter(post=post, full_name='mez', email='test@test.com')

        self.assertEqual(comment[0].comment, 'test test')
        self.assertTrue(comment.exists)
        
    
    def test_edit_and_delete_comments_and_test_there_urls(self):
        
        # get any object for test 
        comment = PostsComment.objects.get_or_create(
            full_name= 'mez',
            email= 'post@post.com',
            comment= 'test test', 
            post=Post.objects.first()
        )[0]

        # get the urls
        edit_comment_url = reverse('EditPostComment', kwargs={'pk':comment.id})
        delete_comment_url = reverse('DeletePostComment', kwargs={'pk':comment.id})

        # test the urls and view
        self.assertEqual(resolve(edit_comment_url).func.view_class, EditPostComment)
        self.assertEqual(resolve(delete_comment_url).func.view_class, DeletePostComment)    

        # get the client and  login

        client =  Client()
        client.login(  
            email = 'post@post.com',
            password = '1234')  


        # test edit comment url with get and post
        response = client.get(
            edit_comment_url
        )
        self.assertEqual(response.status_code, 200)

        # send post request
        response = client.post(
            edit_comment_url, data={
                'full_name': 'hello'
                ,'comment': 'second test',
                'email': 'admin@admin.domain'
            }
        ) 
        self.assertTrue(response.status_code == 302)

        # check if the values change in db
        comment_edited_object = PostsComment.objects.get(id=comment.id)

        self.assertNotEqual(comment.full_name, comment_edited_object.full_name)
        self.assertNotEqual(comment.comment, comment_edited_object.comment)

        # delete this object by post method
        response = client.post(
            delete_comment_url, 
            data={
                'comment_id': comment.id
            }
            )

        self.assertTrue(response.status_code == 302)

        # check again if the object still exist in db
        self.assertFalse(
            PostsComment.objects.filter(id=comment.id).exists()
            )


    def test_create_and_delete_posts_and_test_urls_and_views(self):
        
        # get logged in client
        client =  Client()
        client.login(  
            email = 'post@post.com',
            password = '1234')  

        # get the create url and test it
        create_post_url = reverse('CretePost')
        self.assertEqual(resolve(create_post_url).func.view_class, CretePost)

        # test with get method and authenticated request
        response = client.get(create_post_url)
        self.assertEqual(response.status_code, 200)

        # test with get method and anonymous request
        self.assertEqual(Client().get(create_post_url).status_code, 302)

        # test it with post method and authenticated request
        response = client.post(
            create_post_url, 
            data={
                'image': 'media/assets/images/featured/featured/3rd-image.png',
                'image2': 'media/assets/images/featured/featured/3rd-image.png',
                'title': 'test',
                'text': 'test',                
                'text2': 'test',
                
            }
        )
        self.assertEqual(response.status_code, 200)

        # check it in db
        post = Post.objects.filter(title='test', author__email='post@post.com')
        self.assertTrue(post.exists())
        post_id = post.first().id

        # get and set delete post url
        delete_post_url = reverse('DeletePost', kwargs={'pk': post_id})
        self.assertEqual(resolve(delete_post_url).func.view_class, DeletePost)

        response = client.post(
            delete_post_url
        )

        # check and check in db
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Post.objects.filter(id=post_id).exists()
        )


    def test_edit_posts_and_test_urls_and_views(self):

        # get the url and test 
        url = reverse('UpdatePost', kwargs={'pk': self.post.id})
        self.assertEqual(resolve(url).func.view_class, UpdatePost)

        # check the url with anonymous request
        self.assertEqual(Client().get(url).status_code, 302)

        # check with logged in request
        self.assertEqual(self.client.get(url).status_code, 200)

        response = self.client.post(url,
            data={
                'title':'hello ',
                'text':'hello2222222',
                'text2':'hello2222222', 
                'image':'media/assets/images/featured/featured/3rd-image.png',
                'image2':'media/assets/images/featured/featured/3rd-image.png',
                'author': self.user.id               
            }
        )
        self.assertEqual(response.status_code, 302)

        # check the post in db
        post = Post.objects.get(id=self.post.id)

        self.assertNotEqual(post.title, self.post.title)
        self.assertNotEqual(post.text , self.post.text )
        self.assertNotEqual(post.text2, self.post.text2)
        