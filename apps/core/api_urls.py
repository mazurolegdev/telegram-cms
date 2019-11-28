from django.urls import path
from apps.core.api import backends as api_views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # path('api/v2/telegram_user', api_views.telegram_user),
    # path('api/v2/telegram_user/<int:id>/', api_views.get_telegram_user),
    # path('api/v2/telegram_users', api_views.telegram_users),

    # path('telegram_create_message', api_views.create_message),
]
urlpatterns = format_suffix_patterns(urlpatterns)
