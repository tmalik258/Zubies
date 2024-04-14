from django.contrib import admin

from .models import NewsLetter, BecomeSeller, BecomeSellerImage, BusinessOperation
# Register your models here.
admin.site.register(NewsLetter)
admin.site.register(BecomeSeller)
admin.site.register(BecomeSellerImage)
admin.site.register(BusinessOperation)
