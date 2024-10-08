from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Like, Comment, Account
from .forms import PostForm, CommentForm
from django.views.generic import DeleteView, CreateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import sent

def post_list(request):
    posts =  Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save(commit=False)
            #comment_form.=request.post
            comment_form.user = request.user
            content = request.POST.get('content')
            Comment.objects.create(post=post, user=request.user, content=content)
            comment_form.save()
            return redirect('blog:post_list')
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post,'comments':comments, 'comment_form':comment_form})

def post_new(request):
    if request.method == "POST":
       form = PostForm(request.POST)
       if form.is_valid():
           post = form.save(commit=False)
           post.author = request.user
           post.published_date = timezone.now()
           post.save()
           return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form,'post': post})

class DeletePostView(DeleteView):
    model= Post
    template_name='blog/post_delete.html'
    success_url=reverse_lazy('blog:post_list')

def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
        
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    return redirect('blog:post_list')
    
# def AddCommentView(request,pk):
#     if request.method == "POST":
#        comment = CommentForm(request.POST)
#        if comment.is_valid():
#            text = request.POST.get('body')
#            comment = Comment.objects.create(post=post, user=request.user, content=text)
#            comment.save()
#     else:
#         form = CommentForm()
#     return render(request, 'blog/post_detail.html', {'form': form})

    
    # success_url = reverse_lazy('post_list')


def stat(request):
    x=[]
    user=request.user
    comment =  Comment.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')
    for i in comment:
        if i.post!= None:
            if i.post.author.username == user.username:
                x.append(i.content)
    print(x)
    sent.plot(x,user.username)
    return render(request,'blog/stat.html',{"comment": comment})
