from django.test import TestCase
from django.contrib.auth import get_user_model
from bookmarks.models import Category, Profile
from bookmarks.forms import (
    BookmarkForm,
    EmailChangeForm,
    CustomUserCreationForm
)

User = get_user_model()

class TestForms(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123")

        # Get the Profile created by the post_save signal
        self.profile = Profile.objects.get(user=self.user)

        # Create a test category
        self.category = Category.objects.create(
            user=self.user, category="Test Category")

    def test_profile_and_default_categories_creation(self):
        # Create a new user
        user = User.objects.create_user(
            username="signaluser", email="signal@example.com", password="password123")

        # Check if the profile is created
        self.assertTrue(Profile.objects.filter(user=user).exists())

        # Check if default categories are created
        self.assertTrue(Category.objects.filter(
            user=user, category='Unsorted').exists())
        self.assertTrue(Category.objects.filter(
            user=user, category='Trash').exists())

    def test_bookmark_form_valid(self):
        form_data = {
            'user': self.user.id,  # Ensure this is the user's ID
            'title': 'Test Bookmark',
            'url': 'https://example.com',
            'description': 'A test bookmark',
            'category': self.category.id,  # Ensure this is the category's ID
            'tags': '',  # Tags are optional, so this can be empty
        }
        form = BookmarkForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_email_change_form_valid(self):
        form = EmailChangeForm(data={'email': 'newemail@example.com'})
        self.assertTrue(form.is_valid())

    # def test_email_change_form_invalid_duplicate_email(self):
    #     User.objects.create_user(
    #         username="otheruser", email="newemail@example.com", password="password456")
    #     form = EmailChangeForm(data={'email': 'newemail@example.com'})
    #     self.assertFalse(form.is_valid())
    #     self.assertIn('This email is already in use.', form.errors['email'])

    # def test_custom_user_creation_form_invalid_mismatched_passwords(self):
    #     form_data = {
    #         'username': 'newuser',
    #         'email': 'newuser@example.com',
    #         'password1': 'password123',
    #         'password2': 'differentpassword',  # Deliberately mismatched
    #     }
    #     form = CustomUserCreationForm(data=form_data)
    #     self.assertFalse(form.is_valid())
    #     self.assertIn(
    #         'The two password fields didn’t match.',
    #         form.errors['password2']
    #     )
