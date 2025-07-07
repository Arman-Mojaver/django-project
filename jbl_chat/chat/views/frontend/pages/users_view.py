from __future__ import annotations

from chat.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def users(request: HttpRequest, user_id: int) -> HttpResponse | JsonResponse:
    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    context = {"user_id": user.id, "user_fullname": user.fullname}
    return render(request, "users.html", context)
