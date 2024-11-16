from django.test import TestCase
from django.contrib.auth import get_user_model

from blog.forms import PostModelForm, CommentModelForm

User = get_user_model()

class TestBlogForms(TestCase):

    def test_post_model_form_with_valid_and_invalid_data(self):
        
        # create user as author for post
        user = User.objects.get_or_create(email='admin@admin.domain')[0]
        user.set_password('@Aa12345678')
        user.is_staff = True        
        user.is_superuser = True        
        user.is_verified = True                
        user.save()

        # set form data to validate
        form = PostModelForm(
            {
            'image' : '',
            'image2' : '',
            'title' : 'test',
            'text' : 'test',
            'text2' : 'test',
            'author' : user.id,
            }            
        )

        # check the form
        self.assertTrue(form.is_valid())
        self.assertFalse(PostModelForm().is_valid())

    def test_comment_creation_form_with_valid_and_invalid_data(self):
        
        # send data to form 
        form = CommentModelForm(
            {

                'email': 'maryus19915123@gmail.com',                
                'comment': 'test',                
                'full_name': 'mez',                    
            }
        )

        # check the form
        self.assertTrue(form.is_valid())
        self.assertFalse(CommentModelForm().is_valid())
