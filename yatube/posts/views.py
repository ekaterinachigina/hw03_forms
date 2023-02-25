from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator

from .models import Post, Group, User

from .forms import PostForm

from yatube.settings import POSTS_PER_PAGE


def index(request):
    posts = Post.objects.select_related('author')[:POSTS_PER_PAGE]
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:POSTS_PER_PAGE]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(
        author=author
    ).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = post_list.count()
    context = {
        'author': author,
        'username': username,
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    author = get_object_or_404(Post, pk=post_id)
    post_count = Post.objects.filter(author=author).count()
    context = {
        'author': author,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    context = {
        'form': form,
        'username': request.user
    }
    if form.is_valid():
        post_create = form.save(commit=False)
        post_create.author = request.user
        post_create.save()
        return redirect('posts:profile', username=post_create.author)
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.id != post.author.id:
        return redirect('posts:post_detail', post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        context = {
            'form': form,
            'is_edit': True
        }
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post_id)
        return render(request, 'posts/post_create.html', context)
    form = PostForm(instance=post)
    return render(request, 'posts/post_create.html', context)
