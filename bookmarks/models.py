import logging
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from googleapiclient.discovery import build
from django.conf import settings
from PIL import Image
from io import BytesIO
import os
from .utils import DEFAULT_COLOR


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='bookmarks/images/profiles/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        try:
            old_profile = Profile.objects.get(pk=self.pk)
            old_image_path = old_profile.profile_image.path if old_profile.profile_image else None
        except Profile.DoesNotExist:
            old_image_path = None

        super(Profile, self).save(*args, **kwargs)

        # Delete the old image if a new one is uploaded
        if old_image_path and old_image_path != self.profile_image.path:
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default=DEFAULT_COLOR)
    order = models.PositiveIntegerField(default=0) 

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'category'], name='unique_category_per_user')
        ]
        # Ensure categories are ordered by the 'order' field
        ordering = ['order']

    def __str__(self):
        return self.category


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=10)  # Limit tag length to 10 characters

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'tag'], name='unique_tag_per_user')
        ]

    def __str__(self):
        return self.tag


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    url = models.URLField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)
    uploaded_image = models.ImageField(
        upload_to='bookmarks/images/bookmarks/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def fetch_metadata(self):
        """Fetch metadata such as title, description, and image URL."""
        if not self.title or not self.image_url or not self.description:
            try:
                response = requests.get(self.url, timeout=10)
                response.raise_for_status()
            except Exception:
                return

            soup = BeautifulSoup(response.text, 'html.parser')

            # Set the title
            if not self.title:
                self.title = soup.title.string if soup.title else urlparse(
                    self.url).netloc

            # Set the description
            description_tag = soup.find("meta", attrs={"name": "description"})
            if description_tag and description_tag.get("content"):
                self.description = description_tag["content"]

            domain_name = urlparse(self.url).netloc
            # Get the base domain (e.g., edx.org)
            base_domain = ".".join(domain_name.split(".")[-2:])

            # Attempt to fetch favicon for subdomain
            favicon = soup.find(
                "link", rel=lambda value: value and "icon" in value.lower())
            if favicon and favicon.get("href"):
                favicon_url = favicon["href"]
                if not favicon_url.startswith("http"):
                    favicon_url = urlparse(self.url)._replace(
                        path=favicon_url).geturl()

                if not Bookmark.is_image_pixelated(favicon_url):
                    self.image_url = favicon_url
                    return

            # Fallback to Google Favicon for subdomain
            subdomain_favicon = f'https://www.google.com/s2/favicons?sz=128&domain={domain_name}'
            if not Bookmark.is_image_pixelated(subdomain_favicon):
                self.image_url = subdomain_favicon
                return

            # Fallback to Google Favicon for base domain
            base_domain_favicon = f'https://www.google.com/s2/favicons?sz=128&domain={base_domain}'
            if not Bookmark.is_image_pixelated(base_domain_favicon):
                self.image_url = base_domain_favicon
                return

            # Final fallback: No valid image found
            self.image_url = ''

    def save(self, *args, **kwargs):
        """Overrides save method to fetch metadata before saving."""
        if self._state.adding:
            # Set the order to zero to ensure it appears at the top
            self.order = 0
            # Increment the order of all existing bookmarks for the user
            Bookmark.objects.filter(user=self.user).update(
                order=models.F('order') + 1)
        self.fetch_metadata()
        super(Bookmark, self).save(*args, **kwargs)

    @staticmethod
    def is_image_pixelated(image_url):
        """Checks if the image is too small or likely pixelated."""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            width, height = img.size
            if width < 32 or height < 32:
                return True
        except Exception:
            return True
        return False

    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def create_profile_and_default_categories(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Category.objects.get_or_create(user=instance, category='Unsorted')
        Category.objects.get_or_create(user=instance, category='Trash')
    instance.profile.save()
    

# Disconnect the signal temporarily before loading data
# post_save.disconnect(create_profile_and_default_categories, sender=User)


@receiver(post_delete, sender=Bookmark)
def delete_unused_tags(sender, instance, **kwargs):
    # Get all tags associated with the user
    tags = Tag.objects.filter(user=instance.user)
    for tag in tags:
        # Check if the tag is associated with any bookmarks
        if not tag.bookmark_set.exists():
            tag.delete()


@receiver(post_delete, sender=Profile)
def delete_profile_image(sender, instance, **kwargs):
    if instance.profile_image:
        if os.path.isfile(instance.profile_image.path):
            os.remove(instance.profile_image.path)


@receiver(post_delete, sender=Bookmark)
def delete_bookmark_image(sender, instance, **kwargs):
    if instance.uploaded_image:
        if os.path.isfile(instance.uploaded_image.path):
            os.remove(instance.uploaded_image.path)


@receiver(post_delete, sender=User)
def delete_user_images(sender, instance, **kwargs):
    profile = Profile.objects.filter(user=instance).first()
    if profile and profile.profile_image:
        if os.path.isfile(profile.profile_image.path):
            os.remove(profile.profile_image.path)

    bookmarks = Bookmark.objects.filter(user=instance)
    for bookmark in bookmarks:
        if bookmark.uploaded_image:
            if os.path.isfile(bookmark.uploaded_image.path):
                os.remove(bookmark.uploaded_image.path)
