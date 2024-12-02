from django.contrib import admin
from .models import User, Category, Tag, Bookmark

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Bookmark)
