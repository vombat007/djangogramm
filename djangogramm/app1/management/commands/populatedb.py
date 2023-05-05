from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
import random
from app1.models import User, Post, Image, Like, Hashtag, PostHashtag
from django.utils import timezone
import cloudinary.uploader


class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('number_of_users', type=int, help='Number of fake users to create')
        parser.add_argument('number_of_posts', type=int, help='Number of fake posts to create')
        parser.add_argument('number_of_images_per_post', type=int, help='Number of fake images per post to create')
        parser.add_argument('number_of_likes_per_post', type=int, help='Number of fake likes per post to create')

    def handle(self, *args, **options):
        number_of_users = options['number_of_users']
        number_of_posts = options['number_of_posts']
        number_of_images_per_post = options['number_of_images_per_post']
        number_of_likes_per_post = options['number_of_likes_per_post']

        fake = Faker()

        # create users
        for i in range(number_of_users):
            username = fake.user_name()[:30]
            email = fake.email()[:30]
            password = make_password(fake.password())[:30]
            bio = fake.text()[:200]
            avatar = cloudinary.uploader.upload('https://picsum.photos/468/585',
                                                public_id=f'user-avatar-{i}',
                                                folder='avatars')['secure_url']

            user = User(username=username, email=email, password=password, bio=bio, avatar=avatar)
            user.save()

        # create posts
        users = User.objects.all()
        for i in range(number_of_posts):
            user = random.choice(users)
            caption = fake.text()
            created_at = fake.date_time_between(start_date='-1y', end_date='now',
                                                tzinfo=timezone.get_current_timezone())
            post = Post(user=user, caption=caption, created_at=created_at)
            post.save()

            # create images for the post
            for j in range(number_of_images_per_post):
                image_url = cloudinary.uploader.upload('https://picsum.photos/468/585',
                                                       public_id=f'post-image-{i}-{j}',
                                                       folder='images')['secure_url']
                image = Image(post=post, image_file=image_url)
                image.save()

            # create likes for the post
            likers = list(users.exclude(id=user.id))

            for k in range(number_of_likes_per_post):
                like_user = random.choice(likers)
                like = Like(user=like_user, post=post, created_at=fake.date_time_between(
                    start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone()))
                like.save()

            # create hashtags for the post
            for l in range(random.randint(1, 5)):
                tag = fake.word()
                hashtag, _ = Hashtag.objects.get_or_create(tag=tag)
                post_hashtag = PostHashtag(post=post, hashtag=hashtag)
                post_hashtag.save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully populated the database with {number_of_users} users, '
            f'{number_of_posts} posts, '
            f'{number_of_images_per_post} images per post, and '
            f'{number_of_likes_per_post} likes per post.')
        )
