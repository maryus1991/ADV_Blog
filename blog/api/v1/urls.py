from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import PostModelViewSet, PostCommentModelViewSet

# set the DefaultRouter for PostModelViewSet and PostCommentModelViewSet and separate it to escape the errors and bugs
router = DefaultRouter()
comment_router =  DefaultRouter()

# register the views
router.register('post', PostModelViewSet, basename='post')
comment_router.register('comment', PostCommentModelViewSet, basename='comment')

urlpatterns = [
    path( '', include(router.urls)),

    # set post id for all comments
    path( 'post/<int:post_id>/', include(comment_router.urls))
]




