from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("store.urls", namespace="store")),
    path("account", include("account.urls", namespace="account")),
    path("basket", include("basket.urls", namespace="basket")),
    path("more", include("more.urls", namespace="more")),
    path("order", include("order.urls", namespace="order")),
    path("address", include("address.urls", namespace="address")),
    path("checkout", include("checkout.urls", namespace="checkout")),
]
