from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import (DetailView, 
                                    ListView,  
                                        View,   
                                RedirectView, 
                                  CreateView, 
                                  UpdateView)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Count
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404

import datetime
from utils.get_ip import get_ip

from .models import Post, PostViews, PostsComment
from SiteSetting.models import SiteSetting
from .forms import CommentModelForm, PostModelForm

SiteSetting = SiteSetting.objects.filter(is_active=True).order_by('-id').first

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

    def get_queryset(self):
        """
        for searching in post by word 
        """
        # getting request 
        request = self.request

        # search param in url it gonna return posts thats contains this word in there title or texts
        # if search param not  in url its gonna called the base get queryset func 

        if request.GET.get('search') is not None :
            query = request.GET.get('search')

            return  Post.objects.filter(
                                Q( is_active=True ) ,
                                Q( title__icontains=query ) |
                                Q( text__icontains=query  ) |
                                Q( text2__icontains=query ) 
                                ).all()

        else:
            return super().get_queryset()
    

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

            # getting the parent id and check it not empty
            pid = request.POST.get('parent')
            if pid != '':
                pid = int(pid)
            else: 
                pid = None


            # create the comment 
            PostsComment.objects.create(
                email=form.cleaned_data.get('email'),
                comment=form.cleaned_data.get('comment'),
                full_name=form.cleaned_data.get('full_name'),
                post=self.get_object(),
                parent_id= pid
            )

        # return for the posts
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
        if request.user.is_authenticated:

            # send email and full_name if user is login
            context['comment_form'] = CommentModelForm(initial={
                'email': request.user.email,
            })
        else:
            context['comment_form'] = CommentModelForm()

        
        # adding the most view post
        context['most_view_post'] = Post.objects.order_by('view').annotate(most_view_post_count=Count('view')).all()[:5]

        # adding the parent comments
        context['comments'] = PostsComment.objects.filter(parent=None, post=self.get_object()).prefetch_related('child').all()

        return context
    
    def get_queryset(self): 
        """
        for get the views count and prefetch_related the comment 
        """
        post = Post.objects.annotate(views=Count('view'))
        return post


class DeletePostComment(LoginRequiredMixin, RedirectView):
    '''
    delete the comment if emails is same with Authenticated user email or user is admin or staff user 
    '''

    def get_redirect_url(self,  *args, **kwargs):
        # getting the request and post id
        request = self.request
        post_id = kwargs.get('pk')

        # checking the request method 
        if request.method == 'POST':
            
            # get the comment id from the Post method
            comment_id = request.POST.get('comment_id')

            # check and get the comment if the comment id is not None and exist in db
            if comment_id is not None:
                comment = get_object_or_404(PostsComment, id=comment_id)

                # get the user email and comment email
                comment_email = comment.email
                user_email = request.user.email

                # check if emails from user and comment are same or is admin or star user
                if comment_email == user_email or request.user.is_staff or request.user.is_superuser:
                    
                    # change the comment to not active  and set message
                    comment.is_active = False
                    comment.updated_at = datetime.datetime.now()
                    comment.save()
                    messages.success(
                        request, 
                        'نظر مورد نظر با موقیت حذف شد'
                    )
    
                else:
                    messages.error(
                        request,
                        'شما اجازه حدف این نظر را ندارید'
                    )
            
            else:
                messages.error(
                request,
                'comment not found'
            )

        else:
            messages.error(
                request,
                'مشکلی پیش امده است'
            )

        # get the pk and return the user
        
        return reverse('PostsDetailViews', kwargs={'pk': post_id})


class EditPostComment(LoginRequiredMixin, View):
    """
    for edit the comment if user login with the same email
    """

    def get(self, request, *args, **kwargs):
        # for showing a form for editing the comments and use get_object_or_404 for return 404 error if not exist
        comment = get_object_or_404(PostsComment, id=kwargs.get('pk'))

        # getting user email and check if comment and user email is the same
        email = request.user.email
        if email == comment.email:
            form = CommentModelForm(initial={
                'full_name': comment.full_name,
                'comment' : comment.comment, 
                'email': comment.email

            })

            return render(request, 'blog/editComment.html', {'post': comment.post, 'comment': comment,'comment_form': form})

        else:
            raise Http404()
        

    def post(self, request, *args, **kwargs):
        # get the comment id and get the comment by id
        comment_id = kwargs.get('pk')
        comment = PostsComment.objects.filter(id=comment_id).first()

        # get the form data and validate it
        form = CommentModelForm(request.POST)
        if form.is_valid():

            # checking the comment is exist
            if comment is not None:
                
                # get the post id and request
                post_id = comment.post.id
                
                # get the user email and check if user email and comment email is same
                email = request.user.email
                if email == comment.email:
                    
                    # update the comment 
                    comment.comment = form.cleaned_data.get('comment')
                    comment.full_name = form.cleaned_data.get('full_name')
                    comment.updated_at = datetime.datetime.now()
                    comment.save()

                    # add success message
                    messages.success(
                        request, 
                        'کامنت شما ویرایش شد'
                    )

                else:
                    # add error for not same email
                    messages.error(
                        request,
                        'باید ایمیل مورد نظر باید با ایمیل صاحب ایمیل یکسان باشد تا تایید بشود که صاحب ایمیل شما هستید'
                    )
                
            else:
                # add error for not none error
                messages.error(
                    request,
                    'کامنت پیدا نشد'
                )
            
            
        else:
            # add message for errors
            messages.error(
                request,
                form.errors
            )

        return redirect(reverse('PostsDetailViews', kwargs={'pk': post_id})) 


class CretePost(LoginRequiredMixin, CreateView):
    # create view fo creating post 
    model = Post
    template_name = 'blog/CreateBlog.html'
    form_class = PostModelForm


    def dispatch(self, request, *args, **kwargs):
        """
        *set the dispatch func for check the user is active and verified his account
        """
        if request.user.is_authenticated and    \
                            request.user.is_active and \
                                request.user.is_verified:

            return super().dispatch(request, *args, **kwargs)
        else:
            # set and redirect the user to dashboard if not active and not verify
            messages.error(
                request,
                'لطفا اکانت خود را فعال کنید'
            )

            return redirect(reverse('Dashboard'))

    def form_valid(self, form):
        # set the author id
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):

        # return the form errors
        messages.error(self.request, form.errors)
        response = super().form_invalid(form)
        return response
    
    def get_success_url(self):
        # return the user to post page

        return reverse('PostsDetailViews', kwargs={'pk':self.object.id})
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form_class.author = self.request.user
        return super().get_form(form_class)


# render partial for header and footer

def header_render_partial(request):
    # partial render for header  
    return render(request, 'layouts/Header/Header.html',
            {'SiteSetting': SiteSetting}
        )

def footer_render_partial(request):
    # partial render for footer  
    return render(request, 'layouts/Footer/Footer.html',
        {'SiteSetting': SiteSetting}
    )