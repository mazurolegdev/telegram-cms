from django.conf import settings


# def get_common_apps_path():
#     return f"{os.getcwd()}/apps/common"
#
#
# def change_dir(path):
#     if os.getcwd() != '/app/apps/common':
#         return os.chdir(path)
#     else:
#         return
#
#
# def get_reason_modules_from_path(path):
#     modules = []
#     for dir in os.listdir(path):
#         if os.path.isdir(dir):
#             try:
#                 modules.append(import_module(f'apps.common.{dir}.reasons'))
#             except:
#                 pass
#
#     return modules
#
#
# def get_reasons_list():
#     common_apps_path = get_common_apps_path()
#     common_apps_dir = change_dir(common_apps_path)
#     modules = get_reason_modules_from_path(os.getcwd())
#     return modules
#
#
# def get_class_path_from_reasons_list():
#     modules = get_reasons_list()
#     # print(modules)
#     reasons = []
#
#     for module in modules:
#
#         # print(getattr(module, 'Reason'))
#         try:
#             reasons.append(str(module.Reason.__module__))
#         except:
#             pass
#
#     return reasons

def get_triggers_from_scene(scene):
    triggers = []
    for trigger in scene.triggers.all():
        triggers.append(trigger)

    return triggers


def get_model_lazy(model_name: str):
    from apps.telegram import models
    if model_name == 'trigger':
        return models.Trigger

    elif model_name == 'config':
        return models.Config


def telegram_logger(message, cls=None):
    if settings.DEBUG:
        if type(cls) != str:
            print(f"[telegram-logger][{cls.__str__().split('.')[-1:][0].split(' ')[0]}] {message}")
        else:
            print(f"[telegram-logger][{cls}]")


def get_clear_data(data, param):
    if data:
        if data[param]:
            return data[param]
    else:
        return 0


def parse_message(message):
    # message
    message_id = message['message_id']
    message_mentioned = message['mentioned']
    message_scheduled = message['scheduled']
    message_from_scheduled = message['from_scheduled']
    message_text = message['text']
    message_outgoing = message['outgoing']

    date = message['date']

    # chat
    chat = get_clear_data(message, 'chat')
    chat_id = chat['id']
    chat_title = chat['title']
    chat_username = chat['username']
    chat_permissions = get_clear_data(chat, 'permissions')
    chat_type = get_clear_data(chat, 'type')
    chat_is_verified = get_clear_data(chat, 'is_verified')
    chat_is_restricted = get_clear_data(chat, 'is_restricted')
    chat_is_scam = get_clear_data(chat, 'is_scam')
    chat_photo = get_clear_data(chat, 'photo')

    can_send_messages = get_clear_data(chat_permissions, 'can_send_messages')
    can_send_media_messages = get_clear_data(chat_permissions, 'can_send_media_messages')
    can_send_other_messages = get_clear_data(chat_permissions, 'can_send_other_messages')
    can_add_web_page_previews = get_clear_data(chat_permissions, 'can_add_web_page_previews')
    can_send_polls = get_clear_data(chat_permissions, 'can_send_polls')
    can_change_info = get_clear_data(chat_permissions, 'can_change_info')
    can_invite_users = get_clear_data(chat_permissions, 'can_invite_users')
    can_pin_messages = get_clear_data(chat_permissions, 'can_pin_messages')

    # sender
    sender = get_clear_data(message, 'from_user')
    sender_id = get_clear_data(sender, 'id')
    sender_username = get_clear_data(sender, 'username')
    sender_first_name = get_clear_data(sender, 'first_name')
    sender_last_name = get_clear_data(sender, 'last_name')
    sender_status = get_clear_data(sender, 'status')
    sender_photo = get_clear_data(sender, 'photo')

    sender_is_self = get_clear_data(sender, 'is_self')
    sender_is_contact = get_clear_data(sender, 'is_contact')
    sender_is_bot = get_clear_data(sender, 'is_bot')
    sender_is_verified = get_clear_data(sender, 'is_verified')
    sender_is_scam = get_clear_data(sender, 'is_scam')
    sender_is_support = get_clear_data(sender, 'is_support')
    sender_is_mutual_contact = get_clear_data(sender, 'is_mutual_contact')
    sender_is_deleted = get_clear_data(sender, 'is_deleted')

    if not sender_username:
        print(sender_username)
        print(sender_id)
        print(sender_is_bot)
        print(sender_is_support)
        print(sender_is_scam)
        print(sender_first_name)
        print(sender_last_name)

    result = {
        "message_id": message_id,
        "message_mentioned": message_mentioned,
        "message_scheduled": message_scheduled,
        "message_from_scheduled": message_from_scheduled,
        "message_outgoing": message_outgoing,
        "text": message_text,

        "sender_id": sender_id,
        "sender_username": sender_username,
        "sender_first_name": sender_first_name,
        "sender_last_name": sender_last_name,
        "sender_recently_status": sender_status,
        "sender_photo": sender_photo,
        "sender_is_bot": sender_is_bot,
        "sender_is_contact": sender_is_contact,
        "sender_is_scam": sender_is_scam,
        "sender_is_support": sender_is_support,
        "sender_is_self": sender_is_self,
        "sender_is_verified": sender_is_verified,
        "sender_is_mutual_contact": sender_is_mutual_contact,
        "sender_is_deleted": sender_is_deleted,

        "chat": chat,
        "chat_id": chat_id,
        "chat_type": chat_type,
        "chat_title": chat_title,
        "chat_photo": chat_photo,
        "chat_username": chat_username,
        "chat_is_verified": chat_is_verified,
        "chat_is_restricted": chat_is_restricted,
        "chat_is_scam": chat_is_scam,
        "chat_permissions": {
            "can_send_messages": can_send_messages,
            "can_send_media_messages": can_send_media_messages,
            "can_send_other_messages": can_send_other_messages,
            "can_add_web_page_previews": can_add_web_page_previews,
            "can_send_polls": can_send_polls,
            "can_change_info": can_change_info,
            "can_invite_users": can_invite_users,
            "can_pin_messages": can_pin_messages,
        },
        "message_type": "Incoming",
        "date": date,
    }

    return result


def log(message, level):
    if level == 1:
        level = 'info'
    if level == 2:
        level = 'warning'
    print(f"[pyrogram-log]{[level]}: {message}")
