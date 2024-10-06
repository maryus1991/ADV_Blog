from django.urls import path
from .views import PostsListsViews, PostsDetailViews

urlpatterns = [
    path('', PostsListsViews.as_view()),
    path('id', PostsDetailViews.as_view()),
]
