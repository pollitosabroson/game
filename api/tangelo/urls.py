from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

apps_patterns = [
]

# General api patterns
urlpatterns = [
    path('api/v1/', include(apps_patterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
