import re
import uuid
import random

import requests
from apps.telegram.middlewares import TriggerMiddleware
from apps.telegram.reasons import DefaultTriggerReason
from django.conf import settings
from django.db import models
from importlib import import_module


def models_logger(message):
    if settings.DEBUG:
        print(f"[models-logger]: {message}")


class Config(models.Model):
    session_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=False,
        verbose_name='Название сессии'
    )

    api_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=False,
        verbose_name='API ID'
    )

    api_hash = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=False,
        verbose_name='API Hash'
    )

    access_token = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Токен доступа к API'
    )

    bot_token = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Токен бота (если это бот)'
    )

    is_bot = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Это бот'
    )

    is_active = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Активен (включен)',
        help_text='Изменять вручную не нужно.'
    )

    is_ready = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Готов к использованию',
    )

    def __str__(self):
        return f"Session: {self.session_name}, Active: {self.is_active}"

    def gen_token(self):
        return f'{uuid.uuid1().hex}{uuid.uuid1().hex}'

    def update_token(self):
        self.access_token = self.gen_token()
        self.save()
        return self

    def save(self, *args, **kwargs):
        if not self.access_token:
            self.access_token = self.gen_token()
        return super(Config, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'config'
        verbose_name_plural = 'configs'


class TelegramUser(models.Model):
    tg_user_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name='ID отправителя'
    )

    tg_username = models.CharField(
        db_index=True,
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Телеграм юзер'
    )
    tg_first_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Имя'
    )
    tg_last_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Фамилия'
    )
    tg_recently_status = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Последнее посещение'
    )

    is_bot = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Это бот'
    )
    is_contact = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Юзер из контактов'
    )
    is_scam = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Скомпроментирован'
    )
    is_support = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Это тех. поддержка'
    )

    class Meta:
        verbose_name = 'телеграм юзер'
        verbose_name_plural = 'телеграм юзеры'

    def __str__(self):
        return f"{self.tg_first_name} {self.tg_last_name}"

    @staticmethod
    def create_from_message(sender_id, username, first_name, last_name,
                            recently_status, is_bot, is_contact, is_scam, is_support):
        created_user = TelegramUser.objects.create(
            tg_user_id=sender_id,
            tg_username=username,
            tg_first_name=first_name,
            tg_last_name=last_name,
            tg_recently_status=recently_status,
            is_bot=is_bot,
            is_contact=is_contact,
            is_scam=is_scam,
            is_support=is_support,
        )
        models_logger(f"Created new Telegram user {first_name} {last_name} from message")
        return created_user

    def update_from_message(self, username, first_name, last_name, recently_status,
                            is_bot, is_contact, is_scam, is_support):
        self.tg_username = username
        self.tg_first_name = first_name
        self.tg_last_name = last_name
        self.tg_recently_status = recently_status
        self.is_bot = is_bot
        self.is_contact = is_contact
        self.is_scam = is_scam
        self.is_support = is_support
        self.save()
        models_logger(f"Updated Telegram user {first_name} {last_name} from message")
        return self


class Chat(models.Model):
    tg_chat_id = models.IntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name='ID чата'
    )
    tg_chat_type = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Тип чата, напр. супергруппа'
    )
    tg_chat_title = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Title чата'
    )
    tg_chat_username = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Username чата'
    )

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'

    def __str__(self):
        return f"{self.tg_chat_title}"

    def update_from_message(self, chat_title, chat_type, chat_username):
        self.chat_title = chat_title
        self.chat_type = chat_type
        self.chat_username = chat_username
        self.save()
        models_logger(f"Updated Telegram chat {chat_title} from message")
        return self

    @staticmethod
    def create_from_message(chat_id, chat_type, chat_title, chat_username):
        created_chat = Chat.objects.create(
            tg_chat_id=chat_id,
            tg_chat_type=chat_type,
            tg_chat_title=chat_title,
            tg_chat_username=chat_username,
        )
        models_logger(f"Created Telegram chat {chat_title} from message")
        return created_chat


class Message(models.Model):
    MESSAGE_TYPE_CHOICES = (
        ("Incoming", "Входящее"),
        ("Sent", "Исходящее")
    )

    # TODO Добавить поле app_id/добавить в сериализатор, обновить на вьюхе.
    # Чтоб поле app обновлялось только из функции save, используя айди из app_id

    app = models.ForeignKey(
        "telegram.Config",
        on_delete=models.deletion.SET_NULL,
        default=None,
        null=True,
        blank=True,
        verbose_name='Приложение'
    )

    message_type = models.CharField(
        max_length=255,
        choices=MESSAGE_TYPE_CHOICES,
        default=None,
        null=True,
        blank=True,
        verbose_name='Тип сообщения'
    )
    message_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name='ID сообщения'
    )

    text = models.TextField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Текст сообщения'
    )

    sender_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name='ID отправителя'
    )

    sender_username = models.CharField(
        db_index=True,
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Телеграм юзер'
    )
    sender_first_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Имя'
    )
    sender_last_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Фамилия'
    )
    sender_recently_status = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Последнее посещение'
    )

    sender_is_bot = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Это бот'
    )
    sender_is_contact = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Юзер из контактов'
    )
    sender_is_scam = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Скомпроментирован'
    )
    sender_is_support = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Это тех. поддержка'
    )

    chat_id = models.IntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name='ID чата'
    )
    chat_type = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Тип чата, напр. супергруппа'
    )
    chat_title = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Title чата'
    )
    chat_username = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Username чата'
    )

    timestamp = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return f"ID: {self.message_id}, from: {self.sender_first_name} {self.sender_last_name}"

    def send_message(self):
        data = {"id_to": f"{self.sender_username}", "text": str(self.text)}
        url = f"{settings.ASYNC_SERVER_URL}/message/send"
        response = requests.post(url, data=data)
        if response.status_code != 200:
            return int(response.status_code)
        else:
            return 200

    def get_sender_or_none(self):
        if self.sender_id:
            try:
                return TelegramUser.objects.get(tg_user_id=self.sender_id)
            except TelegramUser.DoesNotExist:
                return None
        else:
            return None

    def get_chat_or_none(self):
        if self.chat_id:
            try:
                return Chat.objects.get(tg_chat_id=self.chat_id)
            except Chat.DoesNotExist:
                return None
        else:
            return None

    def save(self, *args, **kwargs):
        if self.sender_id:
            try:
                sender = TelegramUser.objects.get(tg_user_id=self.sender_id)
                sender.update_from_message(
                    self.sender_username,
                    self.sender_first_name,
                    self.sender_last_name,
                    self.sender_recently_status,
                    self.sender_is_bot,
                    self.sender_is_contact,
                    self.sender_is_scam,
                    self.sender_is_support
                )

            except TelegramUser.DoesNotExist:
                sender = TelegramUser.create_from_message(
                    self.sender_id,
                    self.sender_username,
                    self.sender_first_name,
                    self.sender_last_name,
                    self.sender_recently_status,
                    self.sender_is_bot,
                    self.sender_is_contact,
                    self.sender_is_scam,
                    self.sender_is_support
                )

        if self.chat_id:
            try:
                chat = Chat.objects.get(tg_chat_id=self.chat_id)
                chat.update_from_message(
                    self.chat_title,
                    self.chat_type,
                    self.chat_username
                )
            except:
                Chat.create_from_message(
                    self.chat_id,
                    self.chat_type,
                    self.chat_title,
                    self.chat_username,
                )
        models_logger(f"Saved Telegram message {self.message_id}")
        return super(Message, self).save(*args, **kwargs)


class Middleware(models.Model):
    MIDDLEWARE_CLASS_CHOICES = (
        ("DefaultTriggerReason", "Default Trigger Reason"),
    )

    middleware_type = models.CharField(
        max_length=255,
        choices=MIDDLEWARE_CLASS_CHOICES,
        default=None,
        null=True,
        blank=False,
        verbose_name='Обработчик'
    )

    class Meta:
        verbose_name = 'middleware'
        verbose_name_plural = 'trigger middleware'

    def __str__(self):
        return f"{self.id}: {self.middleware_type}"

    def save(self, *args, **kwargs):
        return super(Middleware, self).save(*args, **kwargs)


class Trigger(Middleware):
    words = models.TextField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Триггерные слова',
        help_text='Через запятую'
    )

    answers = models.TextField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Ответы',
        help_text='Через запятую. \n'
                  'Ответ выбирается случайным образом из указанного списка.'
    )

    is_enabled = models.BooleanField(
        default=True,
        blank=True,
        null=True,
        verbose_name='Активно'
    )

    timestamp = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
    )

    def gen_list_from_answers(self):
        answers = []
        i = str(self.answers).split(',')
        for answer in i:
            if answer[0] == ' ':
                answers.append(answer[1:])
        return answers

    def get_random_answer(self):
        answers = self.gen_list_from_answers()
        return random.choice(answers)

    def gen_list_from_words(self):
        words = []
        l = str(self.words).split(',')
        for word in l:
            if word[0] == ' ':
                words.append(word[1:])
        return words

    def get_reasons_module(self):
        return import_module('apps.telegram.reasons')

    def get_reason(self):
        reason_module = self.get_reasons_module()
        reason = getattr(reason_module, str(self.middleware_type))
        return reason

    def __str__(self):
        return str(self.words)

    def save(self, *args, **kwargs):
        print(self.middleware_type)
        if self.middleware_type == 'DefaultTriggerReason':
            pass
        return super(Trigger, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'триггер'
        verbose_name_plural = 'триггеры'


class BaseScene(models.Model):
    title = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Сценарий'
    )

    app = models.ForeignKey(
        "telegram.Config",
        on_delete=models.deletion.SET_NULL,
        default=None,
        null=True,
        blank=True,
        verbose_name='Приложение'
    )

    triggers = models.ManyToManyField(
        "telegram.Trigger",
        default=None,
        blank=True,
        verbose_name='Триггеры',
    )

    is_enabled = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Активный'
    )

    timestamp = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"id: {self.id}, {self.title}"

    class Meta:
        verbose_name = 'родительская сцена'
        verbose_name_plural = 'родительские сцены'


class SceneInstance(BaseScene):
    is_current_instance = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        help_text='Не доступно для ручного изменения.',
        editable=False,
    )

    is_finished_instance = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        help_text='Не доступно для ручного изменения.',
        editable=False,
    )

    is_message = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        editable=False,
    )

    message_type = models.CharField(
        max_length=255,
        choices=Message.MESSAGE_TYPE_CHOICES,
        default=None,
        null=True,
        blank=True,
        verbose_name='Тип сообщения'
    )
    message_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name='ID сообщения'
    )

    text = models.TextField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Текст сообщения'
    )

    sender_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name='ID отправителя'
    )

    sender_username = models.CharField(
        db_index=True,
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Телеграм юзер'
    )
    sender_first_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Имя'
    )
    sender_last_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Фамилия'
    )

    def __str__(self):
        return f"id: {self.id}, {self.title}, sender_username: {self.sender_username}"

    class Meta:
        verbose_name = 'сцена сообщения'
        verbose_name_plural = 'сцены сообщений'

class History(models.Model):

    subject = models.TextField(
        default=None,
        blank=True,
        null=True,
        verbose_name='Предмет истории'
    )

    is_error = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"id: {self.id}, is_error: {self.is_error}, {self.timestamp}"

    class Meta:
        verbose_name = 'история'
        verbose_name_plural = 'истории'