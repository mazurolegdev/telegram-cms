import uuid

from django.db import models


class Note(models.Model):
    text = models.TextField(
        default=None,
        blank=True,
        null=True,
        verbose_name='Текст записки'
    )

    access_token = models.CharField(
        max_length=255,
        default=None,
        blank=True,
        null=True,
        verbose_name='Токен доступа'
    )

    is_viewed = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Просмотрено'
    )

    timestamp = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.id)

    def gen_token(self):
        return f'{uuid.uuid1().hex}{uuid.uuid1().hex}'

    def update_token(self):
        self.access_token = self.gen_token()
        self.save()
        return self

    def save(self, *args, **kwargs):
        if not self.access_token:
            self.access_token = self.gen_token()
        return super(Note, self).save(*args, **kwargs)

    def pre_delete(self, *args, **kwargs):
        self.is_viewed = True
        self.save()
        return self

    class Meta:
        verbose_name = 'note'
        verbose_name_plural = 'notes'
