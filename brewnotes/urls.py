from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect


def redirect_unknown_url(request, unknown):
    return redirect('home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes.urls')),
    path('accounts/', include('allauth.urls')),
    path('<path:unknown>', redirect_unknown_url),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
