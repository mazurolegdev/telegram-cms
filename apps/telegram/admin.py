from django.contrib import admin
from apps.telegram.models import (
    Config, Message, Chat, TelegramUser, Trigger, Scene, ChatListener
)
from django.http import HttpResponseRedirect
from apps.telegram.main import create_session_from_command_line

admin.site.site_header = 'Telegram CMS v0.1'               # default: "Django Administration"
admin.site.index_title = 'Telegram CMS project'                 # default: "Site administration"
admin.site.site_title = 'Telegram CMS администрирование'        # default: "Django site admin"


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_name', 'api_id', 'api_hash', 'is_bot', 'is_active', 'is_ready')

    # change_list_template = "root/admin/change_list.html"
    change_form_template = 'root/admin/buttons.html'

    def response_change(self, request, obj):
        if "_create_session" in request.POST:
            create_session_from_command_line(int(obj.api_id), str(obj.api_hash), str(obj.session_name))

            self.message_user(request, 'Сессия создана. Соединение с Telegram API установлено.')
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'app', 'is_enabled', 'timestamp')


@admin.register(ChatListener)
class ChatListenerAdmin(admin.ModelAdmin):
    pass


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent_trigger', 'middleware_type', 'is_enabled', 'is_entrypoint_instance',
                    'is_exitpoint_instance', 'is_current_instance', 'is_finished_instance', 'timestamp')

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'tg_user_id', 'tg_username', 'tg_first_name', 'tg_last_name', 'tg_recently_status',
        'is_bot', 'is_contact', 'is_scam', 'is_support',
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('app', 'message_id', 'message_type', )

    # change_form_template = 'root/admin/buttons.html'

    def response_change(self, request, obj):
        if "_send_message" in request.POST:
            try:
                if obj.message_type == 'Sent':
                    result = obj.send_message()
                    if result == 200:
                        self.message_user(request, "Сообщение отправлено")
                        return HttpResponseRedirect(".")
                    else:
                        self.message_user(request, f"Сообщение не отправлено. Код ошибки {result}. "
                                                   f"Асинхронный сервер запущен? Телеграм сессия запущена?")
                        return HttpResponseRedirect(".")
                else:
                    self.message_user(request, "Входящее сообщение не может быть отправлено. Создайте исходящее.")
                    return HttpResponseRedirect(".")
            except:
                self.message_user(request, "Не удалось отправить сообщение")
                return HttpResponseRedirect(".")

        return super().response_change(request, obj)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    pass