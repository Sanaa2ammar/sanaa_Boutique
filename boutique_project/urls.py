# boutique_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),               # الصفحة الرئيسية من تطبيق accounts
    path('products/', include('products.urls')),     # تطبيق المنتجات
    path('cart/', include('cart.urls')),             # تطبيق العربة
    path('categories/', include('categories.urls')), # تطبيق الفئات

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
