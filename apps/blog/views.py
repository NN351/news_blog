from typing import Any, Dict
from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView

from django.shortcuts import get_object_or_404
# Create your views here.

from apps.blog.models import Post, Category, Comment
from apps.blog.forms import CommentForm, PostCreationForm
from apps.blog.filters import PostFilter
# ListView - Это базовый generic класс с помощью которого можно выводить список записей

class PostListView(ListView):
    template_name = "index.html"
    model = Post
    queryset = Post.objects.filter(is_active=True)
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            qs = Post.objects.filter(category__slug=slug)
        else:
            qs = Post.objects.all()
        filter = PostFilter(self.request.GET, qs)
        return filter.qs

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["filter"] = PostFilter(self.request.GET, self.get_queryset())
        return context



class PostDetailView(DetailView):
    template_name = "post_detail.html"
    model = Post
    queryset = Post.objects.filter(is_active=True)
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.META.get('REMOTE_ADDR', None))
        context["comment_form"] = CommentForm()
        return context

# DetailView если его писать в виде функции, пример: 
# def get_detail_post(request, pk):
#     post = get_object_or_404(Post, id=pk)
#     context = {
#         "post":post
#     }
#     return render(request, 'post_detail.html', context)

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

@login_required
def save_comment_form(request, post_id):
    if request.method == "POST":
        print(request.POST)
        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, id=post_id)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect(reverse_lazy("post_detail", kwargs={"pk":post_id}))

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post,id=post_id)
    user = request.user
    if user not in post.likes.all():
        post.likes.add(user)
    else:
        post.likes.remove(user)
    return redirect(reverse_lazy("post_detail", kwargs={"pk":post_id}))


from django.contrib.auth.mixins import LoginRequiredMixin

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name="post_create.html"
    model = Post
    success_url = reverse_lazy("all")
    form_class = PostCreationForm


    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)










