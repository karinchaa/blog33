from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db import transaction
from .forms import CommentForm, PostForm, RegistrationForm, SubscriptionForm, UserProfileForm, ImageForm
from .models import Post, Category, Comment, Subscriber, UserProfile
from django.contrib.auth import login


def get_categories():
    all = Category.objects.all()
    count = all.count()
    return {'cat1': all[0:count // 2 + count % 2], 'cat2': all[count // 2 + count % 2:]}


# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-published_date')  # выборка всех данных
    # posts_id = Post.objects.get(pk=1) #привязка к ид
    # posts = Post.objects.filter(title__contains='Python')
    # posts = Post.objects.filter(published_date__year=2023)
    # categories = Category.objects.all()
    context = {'posts': posts}
    context.update(get_categories())

    return render(request, 'blog/index.html', context=context)


def post(request, id=None):
    post = get_object_or_404(Post, title=id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(post=post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return render(request, "blog/post.html", context={'post': post, 'comment_form': comment_form, 'comments': comments})

    context = {'post': post, 'comments': comments, 'comment_form': comment_form}
    context.update(get_categories())
    return render(request, 'blog/post.html', context=context)


def about(request):
    context = {}
    return render(request, 'blog/about.html', context=context)


def services(request):
    context = {}
    return render(request, 'blog/services.html', context=context)


def contact(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not Subscriber.objects.filter(email=email).exists():
                subscriber = Subscriber(email=email)
                subscriber.save()
            return redirect('subscription_success')
    else:
        form = SubscriptionForm()

    return render(request, 'blog/contact.html', {'form': form})


def subscription_success(request):
    return render(request, 'blog/subscription_success.html')


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context=context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query) | Q(tag__tag__icontains=query)).order_by('-published_date')
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context=context)


@login_required
def create(request):
    ImageFormSet = formset_factory(ImageForm, extra=3)

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, prefix='image')

        if post_form.is_valid() and formset.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()

            for form in formset:
                if form.cleaned_data.get('image'):
                    image = form.cleaned_data['image']
                    post.poster = image
                    post.save()

            return redirect('index')

    else:
        post_form = PostForm()
        formset = ImageFormSet(prefix='image')

    context = {
        'post_form': post_form,
        'formset': formset,
    }

    return render(request, 'blog/create.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()

    return render(request, 'registration/registration_user.html', {'form': form})


def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    return render(request, 'blog/profile.html', {'user_profile': user_profile})


@login_required
def update_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user)
        return redirect('update_profile')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'blog/update_profile.html', {'form': form})
