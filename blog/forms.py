from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import PostsComment

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