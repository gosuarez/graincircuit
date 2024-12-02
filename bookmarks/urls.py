from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bookmarks/", views.bookmarks_view, name="bookmarks"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('settings/', views.settings, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('change_email/', views.change_email, name='change_email'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('update_profile_image/', views.update_profile_image, name='update_profile_image'),
    path('update_username/', views.update_username, name='update_username'),
    path("add/", views.add_bookmark, name="add_bookmark"),
    path("trash/", views.trash, name="trash"),
    path("trash/delete_all/", views.delete_all_bookmarks, name="delete_all_bookmarks"),
    path("trash/<int:bookmark_id>/restore/", views.restore_bookmark, name="restore_bookmark"),
    path("trash/<int:bookmark_id>/delete/", views.delete_forever, name="delete_forever"),
    path("bookmark/<int:bookmark_id>/trash/", views.move_to_trash, name="move_to_trash"),
    path("unsorted/", views.unsorted, name="unsorted"),
    path("bookmark/<int:bookmark_id>/edit/", views.edit_bookmark, name="edit_bookmark"),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:category_name>/', views.bookmarks_by_category, name='bookmarks_by_category'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/<int:category_id>/rename/', views.rename_category, name='rename_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('category/<int:category_id>/edit_color/', views.edit_category_color, name='edit_category_color'),
    path('update_bookmark_order/', views.update_bookmark_order,
         name='update_bookmark_order'),
    path('update_category_order/', views.update_category_order,
         name='update_category_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
