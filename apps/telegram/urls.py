from django.urls import path
from apps.telegram.api import backends as api_views
from rest_framework.urlpatterns import format_suffix_patterns
from apps.telegram import views as telegram_views


api_patterns = [
    path('config/<int:id>/<str:token>/', api_views.get_config),
    path('message', api_views.create_message),
    path('start_all_bots', telegram_views.start_all_bots, name='start-all-bots-url'),
]
api_patterns = format_suffix_patterns(api_patterns)

urlpatterns = [
] + api_patterns
