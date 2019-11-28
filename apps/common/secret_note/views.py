# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
#
# from apps.telegram.middlewares import TriggerMiddleware
# from apps.telegram.models import Trigger
#
# trigger_moddleware = TriggerMiddleware()
#
# @csrf_exempt
# @trigger_moddleware.middleware
# def test_middleware(request):
#     return JsonResponse({"status": "ok"})
