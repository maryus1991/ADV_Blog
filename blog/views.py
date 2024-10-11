from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Post, PostViews, PostsComment
from django.db.models.aggregates import Count
from django.urls import reverse
from utils.get_ip import get_ip
from .forms import CommentModelForm
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

    def post(self, request, *args, **kwargs):
        """
        for creating comment for this post 
        """
        pk = self.kwargs.get('pk')
        form = CommentModelForm(request.POST)
        if form.is_valid():

            try : 
                pid = form.cleaned_data.get('pid') 
            except AttributeError  : 
                pid = None
            except TypeError   : 
                pid = None
                
            PostsComment.objects.create(
                email=form.cleaned_data.get('email'),
                comment=form.cleaned_data.get('comment'),
                full_name=form.cleaned_data.get('full_name'),
                post_id=pk,
                parent_id= pid
            ).save()
        return reverse('PostsDetailViews', kwargs={'pk':pk})



    def get_context_data(self, **kwargs):
        # getting context and request
        context = super().get_context_data(**kwargs)
        request = self.request

        # getting ip
        ip = get_ip(request)

        # create views is its ip is not exist  or returned it if exist
        view =  PostViews.objects.get_or_create(
            
            post=self.get_object(),
            ip=ip,
            user = request.user if request.user.is_authenticated else None
        )
        
        # changing the view count if exist
        if view[1]:
            view[0].count = view[0].count + 1

        # setting the comment form
        context['comment_form'] = CommentModelForm
        
        return context
    
    def get_queryset(self): 
        """
        for get the views count and prefetch_related the comment 
        """
        post = Post.objects.annotate(views=Count('view')).prefetch_related('postscomment_set')
        post.filter(is_active=True, id=self.kwargs['pk']).first()
        return post


# render partial for header and footer

def header_render_partial(request):
    # partial render for header  
    return render(request, 'layouts/Header/Header.html')

def footer_render_partial(request):
    # partial render for footer  
    return render(request, 'layouts/Footer/Footer.html')