from django.contrib import admin
from django.urls import path, include

from apps.core.api.routes import router
from .utils import schema_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', admin.site.urls),

    path('', include(('apps.core.core_urls', 'core'), namespace='core-urls')),
    path('api/core/', include(('apps.core.api_urls', 'core'), namespace='core-api-urls')),
    path('api/telegram/', include(('apps.telegram.urls', 'telegram'), namespace='telegram-urls')),
    path('api/secret_note/', include(('apps.common.secret_note.urls', 'secret_note'), namespace='secret-note-urls')),

    # REST FRAMEWORK URLS
    path('api/v2/', include(router.urls)),

    # SWAGGER URLS
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # REDOC URLS
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
