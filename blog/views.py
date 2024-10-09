from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Post, PostViews
from django.db.models.aggregates import Count
from utils.get_ip import get_ip
# Create your views here.

class PostsListsViews(ListView):
    """
    List views for posts models
    """
    model = Post
    paginate_by = 15
    template_name = 'blog/news-grid.html'
    context_object_name = 'posts'
    ordering = '-id'

class PostsDetailViews(DetailView):
    """
    detail the posts models
    """
    model = Post
    template_name = 'blog/news-details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        ip = get_ip(request)
        post = PostViews.objects.get_or_create(
            post=self.get_object(),
            ip=ip,
            user = request.user if request.user.is_authenticated else None
        )
        
        return context
    
    def get_queryset(self):
        # todo : fix this problem
        return super().get_queryset().annotate(comment_count=Count('postscomment'), views=Count('view')).filter(is_active=True).all()
    

# render partial for header and footer

def header_render_partial(request):
    # partial render for header  
    return render(request, 'layouts/Header/Header.html')

def footer_render_partial(request):
    # partial render for footer  
    return render(request, 'layouts/Footer/Footer.html')