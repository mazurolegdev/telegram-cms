from main.celery import app


class TriggerMiddlewareTasks:

    @staticmethod
    @app.task()
    def pre_task(app_id, trigger_id, sender_id, sender_username, text):
        from apps.telegram.models import Config, Trigger

        app = Config.objects.get(id=app_id)
        trigger = Trigger.objects.get(id=trigger_id)

        if trigger.is_enabled:
            if trigger.reason:
                trigger.reason.start_reason(trigger, sender_id, sender_username, text)

    @staticmethod
    @app.task()
    def post_task():
        print('Init post task')


@app.task()
def start_bots_crawling():
    print('gggggg')
    # requests.get('http://172.23.0.3:8080')


@app.task()
def send_telegram_message(model):
    model.send_message()
    return None

# @app.task
# def trigger_middleware_pre_task(app_id):
#     print(app_id)
# trigger = get_model_lazy('trigger').objects.get(id=trigger_id)
# app = get_model_lazy('config').objects.get(api_id=app_id)

# print(trigger)
# print(app)
