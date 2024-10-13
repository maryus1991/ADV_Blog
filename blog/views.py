from django.shortcuts import redirect, render
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

        form = CommentModelForm(request.POST)
        
        if form.is_valid():


            pid = request.POST.get('parent')
            if pid != '':
                pid = int(pid)
            else: 
                pid = None



            PostsComment.objects.create(
                email=form.cleaned_data.get('email'),
                comment=form.cleaned_data.get('comment'),
                full_name=form.cleaned_data.get('full_name'),
                post=self.get_object(),
                parent_id= pid
            )

        return redirect(reverse('PostsDetailViews', kwargs={'pk': self.get_object().id}))



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
        
        # changing the count of the views
        count = 0 
        if view[0].count is not None:
            count = view[0].count
            
        view[0].count = count  + 1
        view[0].save()

        # setting the comment form
        context['comment_form'] = CommentModelForm
        
        # adding the most view post
        context['most_view_post'] = Post.objects.order_by('-view__count').all()[:5]

        # adding the parent comments
        context['comments'] = PostsComment.objects.filter(parent=None, post=self.get_object()).prefetch_related('child').all()

        return context
    
    def get_queryset(self): 
        """
        for get the views count and prefetch_related the comment 
        """
        post = Post.objects.annotate(views=Count('view')).prefetch_related('postscomment_set')
        return post

# render partial for header and footer

def header_render_partial(request):
    # partial render for header  
    return render(request, 'layouts/Header/Header.html')

def footer_render_partial(request):
    # partial render for footer  
    return render(request, 'layouts/Footer/Footer.html')