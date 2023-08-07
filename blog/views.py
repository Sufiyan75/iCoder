from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Pagination
import math

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all().order_by('?')
    # Pagination:
    rows = 5
    last = math.ceil(len(allPosts)/int(rows))
    page = request.GET.get('page')
    if(not str(page).isnumeric()):
        page=1
    page=int(page)
    allPosts=allPosts[(page-1)*int(rows):(page-1)*int(rows)+int(rows)]
    if (page == 1 and page!=last):
        prev = "#"
        next = "/blog/?page=" + str(page+1)
    elif(page == 1 and page==last):
        prev = '#'
        next = '#'
    elif (page!=1 and page==last):
        prev = "/blog/?page=" + str(page-1)
        next = "#"
    else:
        prev = "/blog/?page=" + str(page-1)
        next = "/blog/?page=" + str(page+1)
    context = {'allPost' : allPosts, 'prev':prev, 'next':next, 'pagecnt':page, 'lastp':last,}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comment = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    
    liked = False
    if request.user.is_authenticated:
        user = request.user
        if post.likes.filter(id=user.id).exists():
            liked=True

    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            if post.likes.filter(id=user.id).exists():
                post.likes.remove(user)
                messages.error(request, "Unliked!")
                liked = False
            else:
                post.likes.add(user)
                messages.success(request, "Liked!")
                liked = True
    context = {'allPost' : post, 'comments' : comment, 'user':request.user, 'replyDict':replyDict, 'liked':liked}
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST['comment']
        user = request.user
        postSno = request.POST['postSno']
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST['parentSno']

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    return redirect(f"/blog/slug/{post.slug}")
