from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import PostsComment, Post


class PostModelForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ( 'image', 'image2', 'title', 'text', 'text2', 'author')
        widgets = {
            'image':forms.FileInput(
                attrs={
                    'placeholder': 'choose your image'
                    ,'class': 'form-control'

                }
            ),            
            'image2':forms.FileInput(
                attrs={
                    'placeholder': 'choose your image'
                    ,'class': 'form-control'

                }
            ),            
            'title':forms.TextInput(
                attrs={
                    'placeholder': 'write your title for post'
                    ,'class': 'form-control'

                }
            ),            
            'text':CKEditorUploadingWidget(
            ),            
            'text2':CKEditorUploadingWidget(
                
            ),
            'author': forms.HiddenInput(
                attrs={
                    'value': '1'
                }
            )                   
        }



class CommentModelForm(forms.Form):
    """
    create comment for posts  
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'name': 'email', 
        'placeholder':"Type Your E-mail...",
        "id": 'validationDefault03'
    }))
    comment = forms.CharField(widget=CKEditorWidget(attrs={
        'name': 'comment', 
        'placeholder':"Type Your Comments...",
        "id": 'validationDefault01', 
        'cols':"30" ,'rows':"10"
    }, config_name='comment'))
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'name': 'full_name', 
        'placeholder':"Type Your full name...",
        "id": 'validationDefault02', 

    }))