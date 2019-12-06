import json

import requests
from django.conf import settings
from django.db import models


class DefaultTriggerReason(models.Model):

    @staticmethod
    def send(response_data):
        response = requests.post(settings.ASYNC_SEND_MESSAGE_URL, data=response_data)

    @staticmethod
    def try_get_child_trigger(trigger):
        if trigger.child_trigger:
            return trigger.child_trigger
        else:
            return None

    @staticmethod
    def run_child_rules(trigger, data, response_data, app, rules):

        if rules['run_child']:
            pass

        elif not rules['run_child']:
            pass

        elif rules['run_child'] == 'try':
            if rules['is_action']:
                pass

            elif not rules['is_action']:
                if rules['is_reverse_action']:
                    pass

        child_trigger = DefaultTriggerReason.try_get_child_trigger(trigger)
        if child_trigger:
            answer = trigger.child_trigger.get_random_answer()
            response_data.update({
                "text": answer,
            })
            DefaultTriggerReason.send(response_data)

    @staticmethod
    def run_instance_rules(trigger, data, app, rules):

        response_data = {
            "id_to": data['sender_id'],
            "session_name": data['session_name'],
            "app_id": data['app_id'],
            "api_hash": data['api_hash'],
            "session_string": str(app.session_string),
            "is_bot_session": data['is_bot_session']
        }

        if rules['is_instance'] == 'entrypoint':
            response_data.update({
                "text": trigger.get_random_answer()
            })
            DefaultTriggerReason.send(response_data)

        if rules['is_instance'] == 'exitpoint':
            response_data.update({
                "text": trigger.get_random_answer()
            })
            DefaultTriggerReason.send(response_data)

        if rules['is_instance']:
            if rules['is_reverse_action']:
                pass

        DefaultTriggerReason.run_child_rules(trigger, data, response_data, app, rules)

    @staticmethod
    def check_words(words, text):
        for word in words:
            if str(word) == str(text):
                return word
        return None

    @staticmethod
    def fetch(trigger, data, app, rules):
        words = trigger.gen_list_from_words()
        word = DefaultTriggerReason.check_words(words, str(data['text']))

        if word:
            DefaultTriggerReason.run_instance_rules(trigger, data, app, rules)

    @staticmethod
    def start(trigger, data, app, current_trigger_instance=None, plugins=None, rules=None):
        if not rules:
            rules = Rules(to=trigger).get()

        return DefaultTriggerReason.fetch(trigger, data, app, rules)

    def __str__(self):
        return f"ID: {self.id}"

    class Meta:
        verbose_name = 'handler'
        verbose_name_plural = 'handlers'


class Rules:
    def __init__(self, to):
        self.trigger = to
        self.rules = {}
        self.check_trigger()

    def check_trigger(self):
        if self.trigger.is_entrypoint_instance:
            self.rules.update({
                "run_child": True,
                "is_instance": "entrypoint",
                "is_action": self.trigger.is_action,
                "is_reverse_action": self.trigger.is_reverse_action,
            })

        elif self.trigger.is_exitpoint_instance:
            self.rules.update({
                "run_child": False,
                "is_instance": "exitpoint",
                "is_action": self.trigger.is_action,
                "is_reverse_action": self.trigger.is_reverse_action,
            })

        else:
            self.rules.update({
                "run_child": "try",
                "is_instance": True,
                "is_action": self.trigger.is_action,
                "is_reverse_action": self.trigger.is_reverse_action,
            })

    def get(self):
        if self.rules:
            return json.loads(json.dumps(self.rules))
        else:
            return None
