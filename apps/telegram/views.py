from django.http import JsonResponse
from apps.telegram.tasks import start_bots_crawling

def start_all_bots(request):
    # start_bots_crawling.delay()
    print('gggggg')
    return JsonResponse({"status": "ok"})