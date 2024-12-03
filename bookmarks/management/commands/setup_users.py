import os
from django.core.management.base import BaseCommand
from bookmarks.models import User 


class Command(BaseCommand):
    help = "Set up the admin and guest users"

    def handle(self, *args, **kwargs):
        self.create_admin_user()
        self.create_guest_user()

    def create_admin_user(self):
        username = os.getenv("ADMIN_USERNAME")
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(
                f"Superuser '{username}' created successfully."))
        else:
            self.stdout.write(self.style.WARNING(
                f"Superuser '{username}' already exists."))

    def create_guest_user(self):
        username = os.getenv("GUEST_USERNAME")
        email = os.getenv("GUEST_EMAIL")
        password = os.getenv("GUEST_PASSWORD")

        if not User.objects.filter(username=username).exists():
            guest_user = User.objects.create_user(
                username=username, email=email, password=password)
            guest_user.is_staff = False  # Ensure guest user has no staff privileges
            guest_user.save()
            self.stdout.write(self.style.SUCCESS(
                f"Guest user '{username}' created successfully."))
        else:
            self.stdout.write(self.style.WARNING(
                f"Guest user '{username}' already exists."))
