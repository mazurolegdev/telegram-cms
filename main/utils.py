import json

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def get_config():
    file = open('/app/config.json', 'r').read()
    config = json.loads(file)
    return config

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)