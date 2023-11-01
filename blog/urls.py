from django.urls import path
from . import views

urlpatterns = [
    path("create-post/", views.BlogPostCreateView.as_view(), name="create-post"),
    path("", views.BlogListView.as_view(), name="post-list"),
    path("update/<int:pk>/", views.BlogPostUpdateView.as_view(), name="post-update"),
    path("<int:pk>/", views.BlogPostDetailView.as_view(), name="post")
]