from rest_framework import routers
from apps.core.api.viewsets import (
    UserViewSet, MessageViewSet,
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register('users', UserViewSet)
# router.register('telegram_users', TelegramUserViewSet)
# router.register('chats', ChatViewSet)
# router.register('messages', MessageViewSet)
