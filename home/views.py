from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime

# Create your views here.
def home(request):
    popular_blog = Post.objects.order_by('-views')[:3]
    context = {'popular_blogs':popular_blog}
    return render(request, 'home/home.html', context)

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)>3 and len(phone)>10 and len(content)>10:
            messages.error(request, "Please fill the detilas correctly!")
        else:
            contacts = Contact(name=name, email=email, phone=phone, content=content)
            contacts.save()
            messages.success(request, "Form Submitted Successfully!")
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query) > 80:
        allPost = Post.objects.none()
    else:
        allPostTitle = Post.objects.filter(title__icontains=query)
        allPostContent = Post.objects.filter(content__icontains=query)
        allPostAuthor = Post.objects.filter(author__icontains=query)
        allPostDate = Post.objects.filter(timeStamp__icontains=query)
        allPost = allPostTitle.union(allPostTitle, allPostContent, allPostAuthor, allPostDate)
    context = {'allPost':allPost, 'query':query}
    return render(request, 'home/search.html', context)

def handlesignup(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your icoder Account has been created successfully!")
        return redirect('/')
    else:
        return HttpResponse("<h1>404 Not Found</h1>")
    
def handlelogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']
        user = authenticate(request, username=loginusername, password=loginpassword)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("/admin")
        elif user is not None and not user.is_staff:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect("/dashboard")
        else:
            messages.error(request, "Invalid credentials, please provide valid details!")
            return redirect("home")
    else:
        return HttpResponse("<h1>404 Not Found</h1>")

def handlelogout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'user/dashboard.html')
    else:
        return HttpResponse("<h1>404 Not Found</h1>")
    
def addBlog(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        author = request.POST['author']
        slug = request.POST['slug']
        image = request.FILES['image']
        try:
            addBlog = Post(title=title, content=content, author=author, slug=slug, image=image, timeStamp=datetime.now(), views=0)
            addBlog.save()
            messages.success(request, "New Blog Added Successfully")
            return redirect(f'/blog/slug/{slug}')
        except Exception as e:
            messages.error(request, 'Something went wrong!')
    return render(request, 'user/addBlog.html')

def profile(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        try:
            myuser = User.objects.filter(username=username).first()
            myuser.username = username
            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.email = email
            myuser.save()
            messages.success(request, 'Personal details updated successfully')
            return render(request, 'user/profile.html')
        except Exception as e:
            messages.error(request, f'Something went wrong!')
        messages.success(request, "Personal details changed successfully!")
        return redirect("profile")
    return render(request, 'user/profile.html')

def viewBlogs(request):
    first_name = request.user.first_name +" "+request.user.last_name
    # print(first_name)
    allPosts = Post.objects.filter(author=first_name)
    context = {'allPost':allPosts}
    # print(allPosts)
    return render(request, 'user/viewBlogs.html', context)

def editBlog(request, slug):
    allPosts = Post.objects.filter(slug=slug).first()
    context = {'allPost':allPosts}
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        author = request.POST['author']
        slug = request.POST['slug']
        try:
            post = Post.objects.filter(slug=slug).first()
            post.title = title
            post.content = content
            post.author = author
            post.slug = slug
            post.save()
            messages.success(request, 'Changes done successfully')
            return redirect(f'/{slug}/editBlog/')
        except Exception as e:
            messages.error(request, f'Something went wrong!')
    return render(request, 'user/editBlog.html', context)