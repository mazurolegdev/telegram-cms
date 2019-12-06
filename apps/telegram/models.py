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
    pass
    # if settings.DEBUG:
    #     print(f"[models-logger]: {message}")


class Config(models.Model):
    session_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=False,
        verbose_name='Session name'
    )
    session_string = models.CharField(
        max_length=1000,
        default=None,
        null=True,
        blank=True,
        # editable=False,
        help_text='Updated automatically'
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
        verbose_name='CMS API Access Token',
        help_text='Updated and created automatically'
    )

    bot_token = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Telegram Bot Token (if bot)'
    )

    is_bot = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name="It's bot"
    )

    is_active = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Is active (on)',
        help_text='Updated automatically.'
    )

    is_ready = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Is ready to use (set it on when app ready to use)',
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
        verbose_name='Sender id'
    )

    tg_username = models.CharField(
        db_index=True,
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Sender username'
    )
    tg_first_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Sender first name'
    )
    tg_last_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Sender last name'
    )
    tg_recently_status = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Recently status'
    )

    is_bot = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name="It's bot"
    )
    is_contact = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='User from contacts'
    )
    is_scam = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Is scam'
    )
    is_support = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Is support'
    )

    class Meta:
        verbose_name = 'telegram user'
        verbose_name_plural = 'telegram users'

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
        verbose_name='Chat id'
    )
    tg_chat_type = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Chat type'
    )
    tg_chat_title = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Chat title'
    )
    tg_chat_username = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Chat username'
    )

    class Meta:
        verbose_name = 'chat'
        verbose_name_plural = 'Chats'

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
        ("Incoming", "Incoming"),
        ("Sent", "Sent")
    )

    # TODO Добавить поле app_id/добавить в сериализатор, обновить на вьюхе.
    # Чтоб поле app обновлялось только из функции save, используя айди из app_id

    app = models.ForeignKey(
        "telegram.Config",
        on_delete=models.deletion.SET_NULL,
        default=None,
        null=True,
        blank=True,
        verbose_name='Application'
    )

    message_type = models.CharField(
        max_length=255,
        choices=MESSAGE_TYPE_CHOICES,
        default=None,
        null=True,
        blank=True,
        verbose_name='Message type'
    )
    message_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Message id'
    )

    text = models.TextField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Message text'
    )

    sender_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Sender id'
    )

    sender_username = models.CharField(
        db_index=True,
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Sender username'
    )
    sender_first_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Sender first name'
    )
    sender_last_name = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Sender last name'
    )
    sender_recently_status = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Recently status'
    )

    sender_is_bot = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name="It's bot"
    )
    sender_is_contact = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Sender in contacts'
    )
    sender_is_scam = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Sender is scam'
    )
    sender_is_support = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name="It's support"
    )

    chat_id = models.IntegerField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Chat id'
    )
    chat_type = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Chat type'
    )
    chat_title = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Chat title'
    )
    chat_username = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Chat username'
    )

    timestamp = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'Messages'

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
        verbose_name='Handler'
    )

    class Meta:
        verbose_name = 'middleware'
        verbose_name_plural = 'trigger middleware'

    def __str__(self):
        return f"{self.id}: {self.middleware_type}"

    def save(self, *args, **kwargs):
        return super(Middleware, self).save(*args, **kwargs)


class Trigger(Middleware):

    title = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Title'
    )

    words = models.TextField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Trigger words',
        help_text='Separated by a comma without spaces in between. '
                  'If left blank, the trigger will become "Executable Immediately".'
                  'He will not wait for the trigger word on entry, but will be executed immediately upon his call.'
                  'Convenient for dynamic dialogue continuation.'
    )

    answers = models.TextField(
        default=None,
        null=True,
        blank=True,
        verbose_name='answers',
        help_text='Separated by a comma. \n'
                  'The answer is randomly selected from the specified list.'
    )

    child_trigger = models.ForeignKey(
        "self",
        on_delete=models.deletion.SET_NULL,
        default=None,
        null=True,
        blank=True,
        related_name='from_child',
        verbose_name='Child trigger'
    )

    parent_trigger = models.ForeignKey(
        "self",
        on_delete=models.deletion.SET_NULL,
        default=None,
        null=True,
        blank=True,
        verbose_name='Parent trigger'
    )

    is_enabled = models.BooleanField(
        default=True,
        blank=True,
        null=True,
        verbose_name='Is Enabled'
    )

    is_entrypoint_instance = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Is entrypoint instance'
    )

    is_exitpoint_instance = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Is exitpoint instance'
    )

    is_current_instance = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Is current instance',
        editable=False
    )

    is_finished_instance = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Is finished instance',
        editable=False
    )

    is_instance = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Instance of the inside of the dialogue',
        help_text='Automatically installed.',
        editable=False
    )

    is_action = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Executable Immediately',
        help_text='If so, the trigger will not wait for the input word. It will be executed immediately upon call. '
                  'Convenient for the dynamic continuation of the dialogue.',
        # editable=False
    )

    is_reverse_action = models.BooleanField(
        default=None,
        null=True,
        blank=True,
        verbose_name='Reverse trigger',
        help_text='It works when the response is sent first and a trigger input is expected after the response. '
                  'Installed automatically',
        # editable=False
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
            # if answer[0] == ' ':
            #     answers.append(answer[1:])
            answers.append(answer)
        return answers

    def get_random_answer(self):
        answers = self.gen_list_from_answers()
        return random.choice(answers)

    def gen_list_from_words(self):
        words = []
        l = str(self.words).split(',')
        for word in l:
            # if word[0] == ' ':
            #     words.append(word[1:])
            # else:
            #     words.append(word)
            words.append(word)
        return words

    def get_reasons_module(self):
        return import_module('apps.telegram.reasons')

    def get_reason(self):
        reason_module = self.get_reasons_module()
        reason = getattr(reason_module, str(self.middleware_type))
        return reason

    def __str__(self):
        return f"id: {self.id}, {self.title}"

    def save(self, *args, **kwargs):
        if self.is_exitpoint_instance:
            self.is_instance = False

        elif self.is_entrypoint_instance:
            self.is_instance = False

        elif not self.is_entrypoint_instance and not self.is_exitpoint_instance:
            self.is_instance = True

        if self.words:
            self.is_action = False

        elif not self.words and self.is_instance:
            self.is_action = True

        if self.is_instance and not self.words:
            self.is_reverse_action = False

        elif self.is_instance and self.words:
            self.is_reverse_action = True

        if self.is_exitpoint_instance:
            self.is_reverse_action = False

        if self.is_entrypoint_instance:
            self.is_reverse_action = False

        return super(Trigger, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'trigger'
        verbose_name_plural = 'triggers'


class Scene(models.Model):
    title = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
        verbose_name='Scene'
    )

    app = models.ForeignKey(
        "telegram.Config",
        on_delete=models.deletion.SET_NULL,
        default=None,
        null=True,
        blank=True,
        verbose_name='Application'
    )

    triggers = models.ManyToManyField(
        "telegram.Trigger",
        default=None,
        blank=True,
        verbose_name='Triggers',
    )

    is_enabled = models.BooleanField(
        default=False,
        null=True,
        blank=True,
        verbose_name='Is enabled'
    )

    timestamp = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"id: {self.id}, {self.title}"

    class Meta:
        verbose_name = 'scene'
        verbose_name_plural = 'scenes'


# class TriggerInstance(Trigger):
#     sender_id = models.PositiveIntegerField(
#         default=None,
#         null=True,
#         blank=True,
#         verbose_name='Sender id'
#     )
#
#     sender_username = models.CharField(
#         db_index=True,
#         max_length=255,
#         default=None,
#         null=True,
#         blank=True,
#         verbose_name='Sender username'
#     )
#
#     def __str__(self):
#         return f"id: {self.id}, {self.title}, sender_username: {self.sender_username}"
#
#     class Meta:
#         verbose_name = 'сцена сообщения'
#         verbose_name_plural = 'сцены сообщений'

class History(models.Model):

    subject = models.TextField(
        default=None,
        blank=True,
        null=True,
        verbose_name='Subject of history',
        help_text='Will be fixed'
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
        verbose_name = 'history'
        verbose_name_plural = 'history'