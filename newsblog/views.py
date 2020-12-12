from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login as userLogin, logout, authenticate
from django.contrib import messages
from django.template import loader
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from newsblog.models import profilepic, article, comments
from django.views.generic import DetailView
from django.core.files.storage import FileSystemStorage

# Create your views here.

def index(request):
    Article = article.objects.all()
    return render(request, 'index.html', {'Article': Article})

def postArticle(request):
    if request.method == "POST":
        title = request.POST.get("title")
        slug = request.POST.get("slug")
        headline = request.POST.get("headline")
        article_image = request.FILES["article_image"]
        content = request.POST.get("content")
        
        PostArticle = article (title=title, slug=slug, headline=headline, article_image=article_image, content=content)

        instance = PostArticle
        instance.user = request.user
        instance.save()
        print("Post saved")

    return redirect("index")

def profile(request):
    img = ''
    if request.user.is_authenticated:
        img = profilepic.objects.filter(user=request.user).values()

    feedback= comments.objects.filter(user=request.user)

    return render(request, 'profile.html', {'feedback':feedback, 'img': img, 'media_url':settings.MEDIA_URL})

def signup(request):
    MyUser = get_user_model()
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')

        myuser = MyUser.objects.create_user(email, name, mobile_number, password)
        myuser.save()
        myuser = authenticate(request, email=email, password=password)

        userLogin(request, myuser)
        print('user created')
        return redirect("index")
    else:
        print('signup failed')
        return redirect(reverse, 'index')

def userlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        myuser = authenticate(request, email=email, password=password)

        if myuser is not None:
            userLogin(request, myuser)
            messages.success(request, 'login success')
            print('login success')
            return redirect('index')
        else:
            messages.success(request, 'login faild')
            print('login failled')
            return redirect('index')
    return render(request, "index.html")

def userlogout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    print("User Logout")
    return redirect('index')

def profilePic(request):
    if request.method == 'POST':
        propic = request.FILES['propic']

        ProfilePicture = profilepic(propic = propic)
        instance = ProfilePicture
        instance.user = request.user
        instance.save()

    print('Dp Saved')
    return render(request, 'profile.html')


def readfull(request, slug):
    
    fullarticle = article.objects.filter(slug=slug).first()
    post = article.objects.filter(slug=slug).first()
    feedback= comments.objects.filter(post=post)

    context={'fullarticle':fullarticle, 'post':post, 'feedback':feedback,}

    return render(request, 'full.html', context)

def postcomment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = article.objects.get(sno= postSno)

        comment = comments(comment = comment, user = user, post = post)
        comment.save()
        print("comment saved")
    return redirect(f"/readfull/{post.slug}")

def dltcomment(request, id):
    comment = comments.objects.get(sno=id)
    comment.delete()
    print("comment deleted")
    return redirect('profile')