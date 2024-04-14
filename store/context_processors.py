from .models import Category, Brand


def navlist(request):
    return {
        'categories': Category.objects.filter(level=0).order_by('id'),
        'brands': Brand.objects.all().order_by('name')
    }
