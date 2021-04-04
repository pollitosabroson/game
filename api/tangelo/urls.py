from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

apps_patterns = [
    path('', include('assignment.urls')),
]

# General api patterns
urlpatterns = [
    path('api/v1/', include(apps_patterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ADD Dcoumentation
schema_view = get_schema_view(
    openapi.Info(
        title="Game API",
        default_version='v1',
        description="API for parse array",
        contact=openapi.Contact(email="jose.alejandro.her.ros@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    path(
        'swagger(?P<format>\.json|\.yaml)',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        '',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]
