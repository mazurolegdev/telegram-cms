from django.urls import path
from apps.common.secret_note.api import backends as api_views
from rest_framework.urlpatterns import format_suffix_patterns
from apps.common.secret_note import views as note_views

api_patterns = [
    path('note', api_views.create_note),
    path('note/<int:id>/<str:access_token>/', api_views.get_note),
    path('test-middleware', api_views.test_middleware, name='test-middleware-url'),
]
api_patterns = format_suffix_patterns(api_patterns)

urlpatterns = [
] + api_patterns
