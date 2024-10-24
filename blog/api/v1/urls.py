from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from .views import PostModelViewSet, PostCommentModelViewSet

router = DefaultRouter()
comment_router =  DefaultRouter()

router.register('post', PostModelViewSet, basename='post')
comment_router.register('comment', PostCommentModelViewSet, basename='comment')

urlpatterns = [
    path( '', include(router.urls)),
    path( 'post/<int:post_id>/', include(comment_router.urls))
]




