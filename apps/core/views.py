from django.http import JsonResponse
from django.shortcuts import render


def base_view(request):
    context = {}
    context.update({"user_is_authenticated": False})

    if request.user.is_authenticated:
        context.update({"user_is_authenticated": True})

    return render(request, 'root/base.html', context)
