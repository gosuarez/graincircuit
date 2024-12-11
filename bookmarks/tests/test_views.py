from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from bookmarks.models import Category, Bookmark
import requests


User = get_user_model()


class TestViews(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.category = Category.objects.create(
            user=self.user, category="Test Category"
        )

    # def test_login_view_valid_credentials(self):
    #     response = self.client.post(reverse('login'), {
    #         'username': 'testuser',
    #         'password': 'password123'
    #     }, follow=True)

    #     # Assert successful login and redirection
    #     self.assertRedirects(response, reverse('bookmarks'))

    # def test_login_view_invalid_credentials(self):
    #     response = self.client.post(reverse('login'), {
    #         'username': 'testuser',
    #         'password': 'wrongpassword'
    #     })

    #     # Assert login failure and error message
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Invalid username and/or password.")

    # def test_logout_view(self):
    #     self.client.login(username='testuser', password='password123')
    #     response = self.client.get(reverse('logout'), follow=True)

    #     # Assert successful logout and redirection
    #     self.assertRedirects(response, reverse('login'))

    @patch('requests.get')
    def test_add_bookmark_valid(self, mock_get):
        # Mock requests.get to simulate a valid URL response
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html><head><title>Test</title></head></html>"

        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('add_bookmark'), {
            'url': 'https://example.com',
            'category': self.category.id,
        }, follow=True)

        # Assert redirection after adding bookmark
        self.assertRedirects(response, reverse('bookmarks'))

        # Assert bookmark creation
        bookmark = Bookmark.objects.filter(
            user=self.user, url='https://example.com')
        self.assertTrue(bookmark.exists())

    @patch('requests.get')
    def test_add_bookmark_invalid_url(self, mock_get):
        # Mock requests.get to raise MissingSchema exception
        mock_get.side_effect = requests.exceptions.MissingSchema("Invalid URL")

        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('add_bookmark'), {
            'url': 'invalid_url',
            'category': self.category.id,
        }, follow=True)

        # Assert redirection to the bookmarks page
        self.assertRedirects(response, reverse('bookmarks'))

        # Check messages if they exist in the context
        if response.context:
            messages = list(response.context.get('messages', []))
            self.assertEqual(len(messages), 1)
            self.assertEqual(
                str(messages[0]),
                "URL is invalid or unreachable. Please check the URL and try again."
            )


    def test_move_to_trash(self):
        bookmark = Bookmark.objects.create(
            user=self.user, url="https://example.com", category=self.category
        )

        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('move_to_trash', args=[bookmark.id]), follow=True)

        # Assert redirection after moving to trash
        self.assertRedirects(response, reverse('bookmarks'))

        # Assert bookmark is moved to trash category
        trash_category = Category.objects.get(user=self.user, category='Trash')
        bookmark.refresh_from_db()
        self.assertEqual(bookmark.category, trash_category)

    def test_delete_forever(self):
        bookmark = Bookmark.objects.create(
            user=self.user, url="https://example.com", category=self.category
        )

        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('delete_forever', args=[bookmark.id]), follow=True)

        # Assert redirection to trash page
        self.assertRedirects(response, reverse('trash'))

        # Assert bookmark is deleted
        self.assertFalse(Bookmark.objects.filter(id=bookmark.id).exists())
        






