# from apps.telegram.utils import get_reasons_list
from django.db import models


class BaseReason(models.Model):
    TRIGGER = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def get_reasons_list(self):
    #     return get_reasons_list()
    #
    # def get_reason_choices():
    #     reasons = get_reasons_list()
    #     l = []
    #     for reason in reasons:
    #         l.append((f"{reason.Reason.__module__}", f"{reason.Reason.__module__}"))
    #
    #     return tuple(l)

    def get_default_reason_choices():
        return tuple(
            [("default_trigger_reason", "default_trigger_reason")],
        )

    @staticmethod
    def start_reason(trigger, sender_id, sender_username, text, plugins=None, rules=None):
        def run():
            words = trigger.gen_dict_from_words()
            for word in words:
                if str(word) in str(text):
                    print(f"TRIGGER: {trigger}")
                    print(f"APP: {trigger.app}")
                    print(f"HERE TRIGGERED WORD: {word}, AND HERE REQUEST TEXT {text}")
                    print("DO WHAT EVER YOU WANT WITH IT")
            # print(type(trigger))
            # print(f"TRIGGER: {trigger}")
            # print(f"WORDS: {words}")
            # print(f"APP: {trigger.app}")
            # # print(f"SENDER_ID: {sender_id}")
            # # print(f"SENDER_USERNAME: {sender_username}")
            # print(f"REQUEST TEXT: {text}")

        if not plugins and not rules:
            return run()

    def __str__(self):
        return f"ID: {self.id}"


    class Meta:
        verbose_name = 'обработчик'
        verbose_name_plural = 'обработчики'
