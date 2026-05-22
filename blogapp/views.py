from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)

from django.contrib.auth import (
    login,
    logout
)

from django.contrib.auth.decorators import login_required

from .models import (
    Post,
    Comment
)

from .forms import (
    PostForm,
    CommentForm
)

from rest_framework import viewsets

from .serializers import (
    PostSerializer,
    CommentSerializer
)


# Home Page
def home(request):

    posts = Post.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'testapp/home.html',
        {'posts': posts}
    )


# Register
def register_view(request):

    form = UserCreationForm()

    if request.method == 'POST':

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect('login')

    return render(
        request,
        'testapp/register.html',
        {'form': form}
    )


# Login
def login_view(request):

    form = AuthenticationForm()

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            return redirect('home')

    return render(
        request,
        'testapp/login.html',
        {'form': form}
    )


# Logout
def logout_view(request):

    logout(request)

    return redirect('home')


# Create Post
@login_required
def create_post(request):

    form = PostForm()

    if request.method == 'POST':

        form = PostForm(
            request.POST
        )

        if form.is_valid():

            post = form.save(
                commit=False
            )

            post.author = request.user

            post.save()

            return redirect('home')

    return render(
        request,
        'testapp/create_post.html',
        {'form': form}
    )


# Update Post
@login_required
def update_post(request, pk):

    post = get_object_or_404(
        Post,
        id=pk
    )

    form = PostForm(
        instance=post
    )

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            instance=post
        )

        if form.is_valid():

            form.save()

            return redirect('home')

    return render(
        request,
        'testapp/update_post.html',
        {
            'form': form
        }
    )


# Delete Post
@login_required
def delete_post(request, pk):

    post = get_object_or_404(
        Post,
        id=pk
    )

    post.delete()

    return redirect('home')


# Post Detail + Comments
@login_required
def post_detail(request, pk):

    post = get_object_or_404(
        Post,
        id=pk
    )

    comments = post.comments.all()

    form = CommentForm()

    if request.method == 'POST':

        form = CommentForm(
            request.POST
        )

        if form.is_valid():

            comment = form.save(
                commit=False
            )

            comment.user = request.user

            comment.post = post

            comment.save()

            return redirect(
                'detail',
                pk=pk
            )

    return render(
        request,
        'testapp/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form
        }
    )


# REST API
class PostViewSet(
    viewsets.ModelViewSet
):

    queryset = Post.objects.all()

    serializer_class = PostSerializer


class CommentViewSet(
    viewsets.ModelViewSet
):

    queryset = Comment.objects.all()

    serializer_class = CommentSerializer