import requests
from django.conf import settings
from django.db import models


class DefaultTriggerReason(models.Model):

    @staticmethod
    def default_trigger_answer(trigger, data):

        words = trigger.gen_list_from_words()
        print(words)
        for word in words:
            print(2)
            if str(word) in str(data['text']):
                print(f"TRIGGER: {trigger}")
                print(f"HERE TRIGGERED WORD: {word}, AND HERE REQUEST TEXT {data['text']}")
                print("DO WHAT EVER YOU WANT WITH IT")

                answer = trigger.get_random_answer()
                response_data = {
                    "id_to": data['sender_id'],
                    "text": answer,
                }
                response = requests.post(settings.ASYNC_SEND_MESSAGE_URL, data=response_data)
                print(response)

    @staticmethod
    def start(trigger, data, plugins=None, rules=None):
        if not plugins and not rules:
            return DefaultTriggerReason.default_trigger_answer(trigger, data)

    def __str__(self):
        return f"ID: {self.id}"

    class Meta:
        verbose_name = 'обработчик'
        verbose_name_plural = 'обработчики'
