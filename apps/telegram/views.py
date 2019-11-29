from apps.telegram.tasks import start_bots_crawling
from django.http import JsonResponse


def start_all_bots(request):
    start_bots_crawling.delay()
    return JsonResponse({"status": "ok"})
