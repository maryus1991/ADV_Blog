from django.shortcuts import render
from django.views.generic import DeleteView, ListView
from .models import Post
# Create your views here.

class PostsListsViews(ListView):
    """
    List views for posts models
    """
    model = Post
    template_name = 'blog/news-grid.html'
    context_object_name = 'posts'

class PostsDetailViews(DeleteView):
    """
    detail the posts models
    """
    model = Post
    template_name = 'blog/news-details.html'

# render partial for header and footer

def header_render_partial(request):
    # partial render for header  
    return render(request, 'layouts/Header/Header.html')

def footer_render_partial(request):
    # partial render for footer  
    return render(request, 'layouts/Footer/Footer.html')