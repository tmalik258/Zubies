from .models import Category


def navlist(request):
    return {
        'categories': Category.objects.filter(level=0).order_by('id'),
    }
