from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Account(models.Model):
    user = models.ForeignKey(
        User,
        db_index=True,
        default=None,
        null=True,
        on_delete=models.deletion.SET_NULL,
        verbose_name='User'
    )

    online = models.BooleanField(
        default=False,
        null=True,
        verbose_name='Online'
    )

    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'

    def __str__(self):
        return f"User: {self.user} online:{self.online}"
