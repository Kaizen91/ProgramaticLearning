from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Author, PostView, Category
from marketing.models import Signup
from django.db.models import Count, Q
from .forms import CommentForm, PostForm, UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

def password_reset(request):
    pass

def login_view(request):
    next = request.GET.get('next')
    most_recent = Post.objects.order_by('-timestamp')[:3]
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form':form,
        'most_recent':most_recent,
    }
    return render(request, "login.html", context)

def register_view(request):
    next = request.GET.get('next')
    most_recent = Post.objects.order_by('-timestamp')[:3]
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form':form,
        'most_recent':most_recent,
    }
    return render(request, "signup.html", context)

def logout_view(request):
    logout(request)
    return redirect('/')

def get_author(user):
    queryset = Author.objects.filter(user=user)
    if queryset.exists():
        return queryset[0]
    return None

def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count("categories__title"))
    return queryset

def index(request):
    featured = Post.objects.filter(featured=True)
    most_recent = Post.objects.order_by('-timestamp')[:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        "object_list": featured,
        'most_recent': most_recent,
    }

    return render(request, "index.html", context)

def blog(request,cat=None):
    query = request.GET.get('q')
    category_count = get_category_count()
    most_recent = Post.objects.order_by("-timestamp")[:3]

    #derive weather the call is from category search, regular serach, or the normal view
    if cat:
        post_list = Post.objects.filter(categories__title=cat)
    elif query:
        post_list = Post.objects.all()
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    else:
        post_list = Post.objects.all()

    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        "queryset": paginated_queryset,
        "page_request_var": page_request_var,
        "most_recent": most_recent,
        "category_count": category_count,
    }
    return render(request, "blog.html", context )

def post(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by("-timestamp")[:3]
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
        return redirect(reverse("post-detail", kwargs ={
            'id': post.id,
    }))

    context = {
        'post': post,
        'most_recent':most_recent,
        'category_count':category_count,
        'form':form,
    }
    return render(request, "post.html", context )

@login_required
def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'form':form,
        'title':title,
    }
    return render(request, "post_create.html", context)
    
@login_required
def post_update(request, id):
    title ='Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'form':form,
        'title':title,
    }
    return render(request, "post_create.html", context)

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))
