import json
import os
import requests
from requests.exceptions import ConnectionError, InvalidURL, Timeout, HTTPError, MissingSchema
from django.views.decorators.cache import never_cache
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db import transaction
from .models import Bookmark, Category, Tag
from .utils import get_color_options, get_default_context, DEFAULT_COLOR
from .forms import ProfileImageForm, EmailChangeForm, UsernameChangeForm, CustomUserCreationForm


def index(request):
    if request.user.is_authenticated:
        return redirect('bookmarks')
    else:
        return HttpResponseRedirect(reverse("login"))


def bookmarks_view(request):
    if request.user.is_authenticated:
        trash_category = Category.objects.filter(
            user=request.user, category='Trash').first()
        bookmarks = Bookmark.objects.filter(user=request.user).exclude(
            category=trash_category).order_by('order')
        page_obj = paginate(request, bookmarks)
        categories = Category.objects.filter(
            user=request.user).exclude(category='Trash')
        context = get_default_context(
            bookmarks=bookmarks,
            categories=categories,
            page_obj=page_obj,
            selected_category='Unsorted',
        )
        return render(request, 'bookmarks/bookmarks.html', context)
    else:
        return HttpResponseRedirect(reverse("login"))


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        messages.error(request, "Invalid username and/or password.")
    return render(request, "bookmarks/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# def register(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))
#         messages.error(request, " ".join(
#             [error for error_list in form.errors.values() for error in error_list]))
#     else:
#         form = CustomUserCreationForm()
#     return render(request, "bookmarks/register.html", {'form': form})

def guest_login(request):
    guest_user = authenticate(username=os.getenv(
        "GUEST_USERNAME"), password=os.getenv("GUEST_PASSWORD"))
    if guest_user:
        login(request, guest_user)
        return redirect("index")
    else:
        messages.error(
            request, "Guest login failed. Please contact the administrator.")
        return redirect("login")


@login_required(login_url='/login/')
def add_bookmark(request):
    if request.user.username == "guest":
        messages.error(
            request, "This is a demo. Guest users cannot add new bookmarks.")
        return redirect(request.GET.get("next", reverse("index")))

    if request.method == "POST":
        url = request.POST.get("url")
        category_id = request.POST.get("category")
        tags = request.POST.get("tags")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except (ConnectionError, InvalidURL, Timeout, MissingSchema):
            messages.error(
                request, "URL is invalid or unreachable. Please check the URL and try again.")
            return redirect(request.GET.get("next", reverse("index")))
        except HTTPError as e:
            messages.error(
                request, f"URL cannot be added due to an HTTP error: {e}")
            return redirect(request.GET.get("next", reverse("index")))

        category = get_object_or_404(Category, id=category_id) if category_id else \
            Category.objects.get_or_create(
                user=request.user, category='Unsorted')[0]

        bookmark = Bookmark.objects.create(
            user=request.user, url=url, category=category)

        if tags:
            tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(
                    user=request.user, tag=tag_name)
                bookmark.tags.add(tag)

        bookmark.save()
        messages.success(request, "Bookmark added successfully.")
        return redirect(request.GET.get("next", reverse("index")))

    return redirect(request.GET.get("next", reverse("index")))



@login_required(login_url='/login/')
def update_category_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            with transaction.atomic():
                for item in data.get('order', []):
                    Category.objects.filter(id=item['id'], user=request.user).update(
                        order=item['position'])
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required(login_url='/login/')
def move_to_trash(request, bookmark_id):
    if request.user.username == "guest":
        messages.error(
            request, "This is a demo. Guest users cannot delete bookmarks.")
        next_url = request.GET.get('next', reverse('index'))
        return redirect(next_url)

    bookmark = get_object_or_404(Bookmark, id=bookmark_id, user=request.user)
    trash_category, created = Category.objects.get_or_create(
        user=request.user, category='Trash')
    bookmark.category = trash_category
    bookmark.save()

    messages.success(request, "Bookmark moved to trash successfully.")
    next_url = request.GET.get('next', reverse('index'))
    return redirect(next_url)



@login_required(login_url='/login/')
def trash(request):
    trash_category = Category.objects.filter(
        user=request.user, category='Trash').first()
    bookmarks = Bookmark.objects.filter(
        user=request.user, category=trash_category).order_by('order')
    page_obj = paginate(request, bookmarks)
    context = get_default_context(
        bookmarks=bookmarks,
        page_obj=page_obj,
        selected_category='Trash',
        is_trash_view=True
    )
    return render(request, 'bookmarks/bookmarks.html', context)


@login_required(login_url='/login/')
def restore_bookmark(request, bookmark_id):
    bookmark = get_object_or_404(Bookmark, id=bookmark_id, user=request.user)
    bookmark.category, created = Category.objects.get_or_create(
        user=request.user, category='Unsorted')
    bookmark.save()
    return HttpResponseRedirect(reverse("trash"))


@login_required(login_url='/login/')
def delete_forever(request, bookmark_id):
    if request.user.username == "guest":
        messages.error(
            request, "This is a demo. Guest users cannot delete bookmarks permanently.")
        return redirect(reverse('trash'))

    bookmark = get_object_or_404(Bookmark, id=bookmark_id, user=request.user)
    bookmark.delete()

    messages.success(request, "Bookmark deleted permanently.")
    return redirect(reverse('trash'))


@login_required(login_url='/login/')
def unsorted(request):
    unsorted_category = Category.objects.filter(
        user=request.user, category='Unsorted').first()
    bookmarks = Bookmark.objects.filter(
        user=request.user, category=unsorted_category).order_by('order')
    page_obj = paginate(request, bookmarks)
    categories = Category.objects.filter(
        user=request.user).exclude(category='Trash')
    context = get_default_context(
        bookmarks=bookmarks,
        categories=categories,
        page_obj=page_obj,
        selected_category='Unsorted',
        is_unsorted_view=True
    )
    return render(request, 'bookmarks/bookmarks.html', context)


@login_required(login_url='/login/')
def categories(request):
    color_options = get_color_options()
    categories = Category.objects.filter(user=request.user).exclude(
        category__in=['Trash', 'Unsorted']).annotate(bookmark_count=Count('bookmark')).order_by('order')

    context = get_default_context(
        categories=categories,
        color_options=color_options,
        is_categories_view=True,
        default_color=DEFAULT_COLOR
    )
    return render(request, 'bookmarks/categories.html', context)


@login_required(login_url='/login/')
def add_category(request):
    if request.user.username == "guest":
        messages.error(
            request, "This is a demo. Guest users cannot add categories.")
        return redirect('categories')

    color_options = get_color_options()

    if request.method == "POST":
        category_name = request.POST.get('category')
        category_color = request.POST.get(
            'color', Category._meta.get_field('color').default)

        if category_name:
            if Category.objects.filter(user=request.user, category__iexact=category_name).exists():
                error_message = f'The category "{
                    category_name}" already exists. Try with a different name.'
                return render(request, 'bookmarks/categories.html', {
                    'error_message': error_message,
                    'selected_color': category_color,
                    'color_options': color_options,
                    'categories': Category.objects.filter(user=request.user).exclude(
                        category__in=['Trash', 'Unsorted']).annotate(bookmark_count=Count('bookmark')).order_by('order'),
                })
            else:
                Category.objects.filter(user=request.user).update(
                    order=F('order') + 1)
                Category.objects.create(
                    user=request.user, category=category_name, color=category_color, order=0)
                messages.success(request, "Category added successfully.")
                return redirect('categories')

    return redirect('categories')


@login_required(login_url='/login/')
def rename_category(request, category_id):
    if request.user.username == "guest":
        messages.error(
            request, "This is a demo. Guest users cannot rename categories.")
        return redirect('categories')

    category = get_object_or_404(Category, id=category_id, user=request.user)
    color_options = get_color_options()

    if request.method == 'POST':
        new_name = request.POST.get('new_category_name')

        if new_name:
            if Category.objects.filter(user=request.user, category__iexact=new_name).exists():
                error_message = f'The category "{
                    new_name}" already exists. Please choose another name.'
                return render(request, 'bookmarks/categories.html', {
                    'error_message': error_message,
                    'selected_color': category.color,
                    'color_options': color_options,
                    'categories': Category.objects.filter(user=request.user).exclude(
                        category__in=['Trash', 'Unsorted']).annotate(bookmark_count=Count('bookmark')).order_by('order'),
                    'show_rename_modal': True,
                    'rename_category_id': category_id
                })
            else:
                category.category = new_name
                category.save()
                messages.success(request, f'Category renamed to "{new_name}".')
                return redirect('categories')

    return redirect('categories')


@login_required(login_url='/login/')
def delete_category(request, category_id):
    if request.user.username == "guest":
        messages.error(
            request, "This is a demo. Guest users cannot delete categories.")
        return redirect('categories')

    category = get_object_or_404(Category, id=category_id, user=request.user)

    trash_category = Category.objects.filter(
        user=request.user, category='Trash').first()
    if not trash_category:
        trash_category = Category.objects.create(
            user=request.user, category='Trash')

    bookmarks = Bookmark.objects.filter(category=category)
    if bookmarks.exists():
        bookmarks.update(category=trash_category)

    category.delete()
    messages.success(request, f'Category "{category.category}" deleted successfully.')
    return redirect('categories')


@login_required(login_url='/login/')
def edit_category_color(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        new_color = request.POST.get('color')
        if new_color:
            category.color = new_color
            category.save()
    return redirect('categories')


@login_required(login_url='/login/')
def edit_bookmark(request, bookmark_id):
    if request.user.username == "guest":
        messages.error(
            request, "This is a demo. Guest users cannot edit bookmarks.")
        return redirect(request.GET.get("next", reverse("index")))

    bookmark = get_object_or_404(Bookmark, id=bookmark_id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        tags = request.POST.get('tags')
        url = request.POST.get('url')

        if request.FILES.get('image'):
            bookmark.uploaded_image = request.FILES['image']

        bookmark.title = title
        bookmark.description = description
        bookmark.url = url

        if category_id:
            category = Category.objects.get(id=category_id)
            bookmark.category = category

        bookmark.tags.clear()

        if tags:
            tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
            existing_tags = Tag.objects.filter(
                user=request.user, tag__in=tag_names)
            new_tags = [tag_name for tag_name in tag_names if not existing_tags.filter(
                tag=tag_name).exists()]
            for tag_name in new_tags:
                tag, created = Tag.objects.get_or_create(
                    user=request.user, tag=tag_name)
                bookmark.tags.add(tag)
            bookmark.tags.add(*existing_tags)

        bookmark.save()
        messages.success(request, "Bookmark updated successfully.")
        return redirect(request.GET.get("next", reverse("index")))

    return redirect(request.GET.get("next", reverse("index")))



@login_required(login_url='/login/')
def bookmarks_by_category(request, category_name):
    if request.user.is_authenticated:
        category = get_object_or_404(
            Category, user=request.user, category__iexact=category_name.lower()
        )
        bookmarks = Bookmark.objects.filter(
            user=request.user, category=category).order_by('order')
        page_obj = paginate(request, bookmarks)
        categories = Category.objects.filter(
            user=request.user).exclude(category='Trash')

        context = get_default_context(
            bookmarks=bookmarks,
            categories=categories,
            page_obj=page_obj,
            selected_category=category,
            is_category_view=True
        )
        return render(request, "bookmarks/bookmarks.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))


def paginate(request, bookmarks, num=20):
    paginator = Paginator(bookmarks, num)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required(login_url='/login/')
def change_email(request):
    # Restrict guest users
    if request.user.username == "guest":
        return JsonResponse({'success': False, 'message': "This is a demo. Guest users cannot change their email."}, status=403)

    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Your email has been updated successfully.', 'email': request.user.email})
        else:
            # Collect errors from the form
            errors = [error for error_list in form.errors.values()
                      for error in error_list]
            return JsonResponse({'success': False, 'message': " ".join(errors)}, status=400)

    return JsonResponse({'success': False, 'message': "Invalid request."}, status=400)


@login_required(login_url='/login/')
def change_password(request):
    # Restrict guest users
    if request.user.username == "guest":
        return JsonResponse({
            'success': False,
            'message': "This is a demo. Guest users cannot change their password."
        }, status=403)

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            return JsonResponse({
                'success': True,
                'message': "Password changed successfully."
            })
        else:
            # Extract error messages for invalid form submissions
            errors = [error for field_errors in form.errors.values()
                      for error in field_errors]
            return JsonResponse({
                'success': False,
                'message': " ".join(errors)
            }, status=400)

    return JsonResponse({
        'success': False,
        'message': "Invalid request method."
    }, status=400)


@login_required(login_url='/login/')
def delete_account(request):
    if request.method == 'POST':
        if request.user.username == "guest":
            return JsonResponse(
                {'success': False, 'message': "This is a demo. Guest users cannot delete their account."},
                status=403
            )
        # Add the success message to the session
        messages.success(
            request, "Your account has been deleted successfully."
        )
        # Delete the user account
        user = request.user
        user.delete()

        # Log out the user
        logout(request)

        # Redirect to the login page
        return JsonResponse(
            {'success': True, 'redirect_url': reverse('login')}
        )

    return JsonResponse({'success': False, 'message': "Invalid request method."}, status=405)


@login_required(login_url='/login/')
def update_profile_image(request):
    # Restrict guest users
    if request.user.username == "guest":
        return JsonResponse({'success': False, 'message': "This is a demo. Guest users cannot change the profile image."}, status=403)

    if request.method == 'POST' and request.FILES.get('profile_image'):
        form = ProfileImageForm(
            request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'image_url': request.user.profile.profile_image.url})
    return JsonResponse({'success': False, 'message': 'No image uploaded.'}, status=400)


@login_required(login_url='/login/')
def update_username(request):
    # Restrict guest users
    if request.user.username == "guest":
        return JsonResponse({'success': False, 'message': "This is a demo. Guest users cannot change their username."}, status=403)

    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': "Your username has been updated successfully."})
        else:
            # Extract error messages for invalid form submissions
            errors = [error for error_list in form.errors.values()
                      for error in error_list]
            return JsonResponse({'success': False, 'message': " ".join(errors)}, status=400)

    return JsonResponse({'success': False, 'message': "Invalid request."}, status=400)


@login_required(login_url='/login/')
def delete_all_bookmarks(request):
    if request.user.username == "guest":
        messages.error(
            request, "This is a demo. Guest users cannot delete all bookmarks.")
        return HttpResponseRedirect(reverse("trash"))

    trash_category = Category.objects.filter(
        user=request.user, category='Trash').first()
    if trash_category:
        Bookmark.objects.filter(
            user=request.user, category=trash_category).delete()
        messages.success(
            request, "All bookmarks in trash deleted successfully.")

    return HttpResponseRedirect(reverse("trash"))



@login_required(login_url='/login/')
def profile(request):
    return render(request, "bookmarks/profile.html")


@login_required(login_url='/login/')
def settings(request):
    return render(request, "bookmarks/settings.html")


@require_POST
def update_bookmark_order(request):
    try:
        data = json.loads(request.body)
        order = data.get('order')

        if not isinstance(order, list) or not all(isinstance(item, int) for item in order):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        with transaction.atomic():
            for index, bookmark_id in enumerate(order):
                Bookmark.objects.filter(
                    id=bookmark_id, user=request.user).update(order=index)

        return JsonResponse({'success': True})
    except Bookmark.DoesNotExist:
        return JsonResponse({'error': 'Bookmark not found'}, status=404)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    
    
