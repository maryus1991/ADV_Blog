from django.urls import path
from .views import PostsListsViews, PostsDetailViews

urlpatterns = [
    path('', PostsListsViews.as_view(), name='PostsListsViews'),
    path('<int:pk>', PostsDetailViews.as_view(), name='PostsDetailViews'),
]
