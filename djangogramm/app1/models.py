from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models, IntegrityError
from cloudinary.models import CloudinaryField


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')

        if User.objects.filter(email=self.normalize_email(email).lower()).exists():
            raise ValueError('This email has already been registered.')

        user = self.model(
            email=self.normalize_email(email).lower(),
        )

        user.set_password(password)
        try:
            user.save(using=self._db)

        except IntegrityError:
            raise ValueError('This email has already been registered.')

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        error_messages={
            'unique': "This email has already been registered.",
        }
    )
    username = models.CharField(max_length=35)
    password = models.CharField(max_length=255)
    bio = models.TextField(max_length=300)
    avatar = CloudinaryField('avatars')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Custom: was this email validated, at some point, by sending an email?
    is_email_validated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'app1'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.likes.count()

    class Meta:
        app_label = 'app1'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image_file = CloudinaryField('images')

    class Meta:
        app_label = 'app1'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'app1'


class Hashtag(models.Model):
    tag = models.CharField(max_length=25)

    class Meta:
        app_label = 'app1'


class PostHashtag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)

    class Meta:
        app_label = 'app1'
        unique_together = ('post', 'hashtag')
