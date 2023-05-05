from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.db import IntegrityError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Post, User, PostHashtag, Hashtag, Like, UserFollowing, Image
from .forms import ImageForm, RegisterUserForm, LoginForm
from django.http import JsonResponse


def index(request):
    images = Image.objects.all()
    return render(request, 'app1/index.html', {'images': images})


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            try:
                # Create user object but don't save it yet
                user = form.save(commit=False)
                user.is_active = False  # User can't log in until they confirm their email
                user.save()

                # Send email to user with confirmation link
                current_site = get_current_site(request)
                subject = 'Confirm your email'
                confirmation_link = request.build_absolute_uri(
                    reverse('confirm_email', args=[urlsafe_base64_encode(force_bytes(user.pk)),
                                                   default_token_generator.make_token(user)]))
                html_message = render_to_string('app1/confirmation_email.html', {
                    'user': user,
                    'confirmation_link': confirmation_link,
                    'domain': current_site.domain,
                })
                plain_message = strip_tags(html_message)
                from_email = 'DjangoGramm <vombat007@gmail.com>'
                to_email = form.cleaned_data['email']
                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

                return render(request, 'app1/email_confirm.html')
            except IntegrityError:
                form.add_error('username', 'This username is already taken.')
    else:
        form = RegisterUserForm()
    return render(request, 'app1/register.html', {'form': form})


def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'app1/email_confirmed.html')
    else:
        return render(request, 'app1/email_confirm_error.html')


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return render(request, 'app1/login.html', {'error_message': 'Invalid username or password.'})
    else:
        form = LoginForm(request=request)
    return render(request, 'app1/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def user_profile(request, username=None):
    if request.user.is_authenticated:
        user = request.user

        if username is None:
            profile = User.objects.get(username=user.username)
        else:
            profile = User.objects.get(username=username)

        follow = UserFollowing.objects.filter(user=user, following_user=profile).first()

        following_user = UserFollowing.objects.filter(user_id=user)

        followers = UserFollowing.objects.filter(following_user_id=profile)

        return render(request, 'app1/user_profile.html', {
            'profile': profile, 'follow': follow, 'following': following_user, 'followers': followers})

    else:
        return redirect('login')


def following(request, username):
    following_id = User.objects.get(username=username)

    if request.user.is_authenticated:

        user = request.user

        follow = UserFollowing.objects.filter(user=user.id, following_user=following_id.id).first()

        if follow:
            follow.delete()

        else:
            follow = UserFollowing.objects.create(user=user, following_user=following_id)
            follow.save()

    return redirect('profile', following_id.username)


def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        # Update user's profile data
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.bio = request.POST['bio']

        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']

        user.save()
        return redirect('profile')

    profile = User.objects.get(username=user.username)
    return render(request, 'app1/edit_profile.html', {'profile': profile})


def change_password(request):
    user = request.user
    error_message = ''

    if request.method == 'POST':
        # Update user's password
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return redirect('profile')
        else:
            error_message = 'Incorrect password.'

    return render(request, 'app1/change_password.html', {'error_message': error_message})


def post_page(request):
    posts = Post.objects.select_related('user').prefetch_related(
        'images', 'likes', 'posthashtag_set__hashtag').all()

    liked_posts = []
    if request.user.is_authenticated:
        user = request.user
        liked_posts = [liked.post_id for liked in Like.objects.filter(user=user)]
    return render(request, 'app1/post.html', {'posts': posts, 'liked_posts': liked_posts})


def following_post(request):
    if request.user.is_authenticated:
        user = request.user
        follow = UserFollowing.objects.filter(user=user).values_list('following_user__id', flat=True)
        posts = Post.objects.select_related('user').prefetch_related(
            'images', 'likes', 'posthashtag_set__hashtag').filter(user__in=follow).order_by('-created_at')
        return render(request, 'app1/post.html', {'posts': posts})
    else:
        return redirect('login')


def like(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        liked_post = Like.objects.filter(user=user, post=post).first()
        if liked_post:
            liked_post.delete()
        else:
            Like.objects.create(user=user, post=post)
        like_count = post.like_count()
        return JsonResponse({'like_count': like_count})
    else:
        return JsonResponse({'error': 'Invalid request'})


def create_post(request):
    if request.method == 'POST':
        user = request.user
        caption = request.POST.get('caption')
        tags = request.POST.get('tags')
        form = ImageForm(request.POST, request.FILES)

        # Create the post object
        post = Post.objects.create(user=user, caption=caption)

        # Save the images
        image_files = request.FILES.getlist('image_file')
        if len(image_files) > 5:
            error_message = "You can upload at most 5 images."
            return render(request, 'app1/create_post.html', {'form': form, 'error_message': error_message})

        for file in image_files:
            image = Image(post=post, image_file=file)
            image.save()

        # Add hashtags to the post
        if tags:
            tags = tags.split(',')
            for tag in tags:
                hashtag, created = Hashtag.objects.get_or_create(tag=tag.strip())
                PostHashtag.objects.create(post=post, hashtag=hashtag)

        return redirect('post')
    else:
        form = ImageForm()
    return render(request, 'app1/create_post.html', {'form': form})
