from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from .models import Post, SaveBirth
from .forms import PostForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import datetime


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@csrf_exempt
def save_birth(request):
    user_name = request.POST.get("user_name", None)
    birthday = request.POST.get("text", None)

    birth_day = datetime.datetime.strptime(birthday, "%Y/%M/%d").date()

    SaveBirth.objects.create(
        name=user_name,
        birth_day=birth_day,
    )

    return JsonResponse({
        'text': 'created',
        'message' : user_name,
        'birthday' : birth_day,
    })
