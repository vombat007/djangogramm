from django.test import TestCase
from app1.models import User, Post, Image, Like, Hashtag, PostHashtag, UserFollowing


def create_user():
    return User.objects.create(
        username='testuser',
        email='testuser@example.com',
        password='password',
        bio='This is a test bio',
        avatar='path/to/avatar.png'
    )


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = create_user()

    def test_user_creation(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.password, 'password')
        self.assertEqual(user.bio, 'This is a test bio')
        self.assertEqual(user.avatar.url, 'http://res.cloudinary.com/dg4tzo4pz/image/upload/v1/path/to/avatar.png')


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.post = Post.objects.create(
            user=self.user,
            caption='This is a test caption'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.caption, 'This is a test caption')


class ImageModelTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.post = Post.objects.create(
            user=self.user,
            caption='This is a test caption'
        )
        self.image = Image.objects.create(
            post=self.post,
            image_file='path/to/image.png'
        )

    def test_image_creation(self):
        self.assertEqual(self.image.image_file, 'path/to/image.png')


class LikeModelTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.post = Post.objects.create(
            user=self.user,
            caption='This is a test caption'
        )
        self.like = Like.objects.create(
            user=self.user,
            post=self.post
        )

    def test_like_creation(self):
        self.assertEqual(self.like.post, self.post)


class HashtagModelTestCase(TestCase):
    def setUp(self):
        self.hashtag = Hashtag.objects.create(
            tag='testtag'
        )

    def test_hashtag_creation(self):
        self.assertEqual(self.hashtag.tag, 'testtag')


class PostHashtagModelTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.post = Post.objects.create(
            user=self.user,
            caption='Test post',
        )
        self.hashtag = Hashtag.objects.create(
            tag='test'
        )
        self.post_hashtag = PostHashtag.objects.create(
            post=self.post,
            hashtag=self.hashtag,
        )

    def test_post_hashtag_creation(self):
        self.assertEqual(self.post_hashtag.post, self.post)


class UserFollowingModelTest(TestCase):
    def setUp(self):
        self.user1 = create_user()
        self.user2 = User.objects.create(
            username='testuser2',
            email='testuser2@example.com',
            password='password',
            bio='This is a test bio',
            avatar='path/to/avatar.png'
        )
        self.follow = UserFollowing.objects.create(
            user=self.user1,
            following_user=self.user2,
        )

    def test_following(self):
        self.assertEqual(self.follow.user, self.user1)
        self.assertEqual(self.follow.following_user, self.user2)
