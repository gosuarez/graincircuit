# Default category colors

# utils.py
DEFAULT_COLOR = '#1E90FF'

def get_color_options():
    return [
        ('blue', DEFAULT_COLOR),
        ('red', '#B22222'),
        ('coral', '#FF7F50'),
        ('green', '#429c71'),
        ('purple', '#3A3EC5'),
        ('yellow', '#D4AF37'),
        ('magenta', '#FF4FC4'),
        ('dark', '#2F2C32'),
    ]


def get_default_context(**kwargs):
    context = {
        'is_category_view': False,
        'is_categories_view': False,
        'is_trash_view': False,
        'is_unsorted_view': False,
    }
    context.update(kwargs)
    return context


