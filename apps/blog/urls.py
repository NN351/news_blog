from django.urls import path

from apps.blog import views

urlpatterns = [
    path('', views.PostListView.as_view(), name="all"),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),
    path('post/list/<str:slug>/', views.PostListView.as_view(), name="post_list"),
    path('post/comment/save/<int:post_id>/', views.save_comment_form, name="save_comment"),
    path("post/like/<int:post_id>/", views.like_post, name="like_post"),

    path("post/create/", views.PostCreateView.as_view(), name="post_create"),
]