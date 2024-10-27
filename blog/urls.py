from django.urls import path, include
from .views import PostsListsViews, PostsDetailViews, DeletePostComment , EditPostComment

urlpatterns = [
    path('', PostsListsViews.as_view(), name='PostsListsViews'),
    path('<int:pk>', PostsDetailViews.as_view(), name='PostsDetailViews'),
    path('delete-comment/<int:pk>', DeletePostComment.as_view(), name='DeletePostComment'),
    path('edit-comment/<int:pk>', EditPostComment.as_view(), name='EditPostComment'),
    path('post/api/v1/', include('blog.api.v1.urls'))
]
