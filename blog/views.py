from django.shortcuts import render
from django.views.generic import TemplateView, ListView

# Create your views here.

class PostsListsViews(TemplateView):
    """
    List views for posts models
    """
    template_name = 'blog/news-grid.html'

class PostsDetailViews(TemplateView):
    """
    detail the posts models
    """
    template_name = 'blog/news-details.html'

# render partial for header and footer

def header_render_partial(request):
    # partial render for header  
    return render(request, 'layouts/Header/Header.html')

def footer_render_partial(request):
    # partial render for footer  
    return render(request, 'layouts/Footer/Footer.html')