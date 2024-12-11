from django.db import IntegrityError
from django.contrib.auth import get_user_model
from bookmarks.models import Profile, Category, Tag, Bookmark
from django.test import TestCase

User = get_user_model()


class TestBookmarkModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.category = Category.objects.create(
            user=self.user, category="Test Category"
        )
        self.bookmark = Bookmark.objects.create(
            user=self.user, url="https://example.com", category=self.category
        )

    def test_fetch_metadata(self):
        self.bookmark.fetch_metadata()
        self.assertIsNotNone(self.bookmark.title)
        self.assertIsNotNone(self.bookmark.description)
        self.assertIsNotNone(self.bookmark.image_url)

    # def test_is_image_pixelated(self):
    #     # Simulate pixelated and non-pixelated image URLs
    #     small_image_url = "https://via.placeholder.com/20"
    #     large_image_url = "https://via.placeholder.com/128"

    #     self.assertTrue(Bookmark.is_image_pixelated(small_image_url))
    #     self.assertFalse(Bookmark.is_image_pixelated(large_image_url))


class TestSignals(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.category = Category.objects.create(
            user=self.user, category="Test Category"
        )

    def test_profile_and_default_categories_creation(self):
        user = User.objects.create_user(
            username="signaluser", email="signal@example.com", password="password123"
        )
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertTrue(Category.objects.filter(
            user=user, category="Unsorted").exists())
        self.assertTrue(Category.objects.filter(
            user=user, category="Trash").exists())

    # def test_delete_unused_tags(self):
    #     tag = Tag.objects.create(user=self.user, tag="test")
    #     bookmark = Bookmark.objects.create(
    #         user=self.user, url="https://example.com", category=self.category
    #     )
    #     bookmark.tags.add(tag)
    #     bookmark.delete()

    #     self.assertFalse(Tag.objects.filter(tag="test").exists())

    # def test_delete_profile_image(self):
    #     profile = Profile.objects.get(user=self.user)
    #     # Simulate an image being set
    #     profile.profile_image = "test_image.jpg"
    #     profile.save()
    #     profile.delete()

    #     # Simulate file deletion check (would need mocking in production)
    #     # os.path.exists is skipped because test files are not saved
    #     self.assertFalse(Profile.objects.filter(user=self.user).exists())

    # def test_delete_bookmark_image(self):
    #     bookmark = Bookmark.objects.create(
    #         user=self.user, url="https://example.com", category=self.category
    #     )
    #     # Simulate an uploaded image
    #     bookmark.uploaded_image = "test_bookmark_image.jpg"
    #     bookmark.save()
    #     bookmark.delete()

    #     # Simulate file deletion check
    #     self.assertFalse(Bookmark.objects.filter(pk=bookmark.pk).exists())


class TestConstraints(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )

    def test_unique_category_per_user(self):
        Category.objects.create(user=self.user, category="Unique Category")
        with self.assertRaises(IntegrityError):
            Category.objects.create(user=self.user, category="Unique Category")

    def test_unique_tag_per_user(self):
        Tag.objects.create(user=self.user, tag="Unique Tag")
        with self.assertRaises(IntegrityError):
            Tag.objects.create(user=self.user, tag="Unique Tag")


class TestModelStr(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.category = Category.objects.create(
            user=self.user, category="Category Name")
        self.bookmark = Bookmark.objects.create(
            user=self.user, url="https://example.com", category=self.category
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Category Name")

    def test_bookmark_str(self):
        self.assertEqual(str(self.bookmark), self.bookmark.title)

    def test_profile_str(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), "testuser Profile")


