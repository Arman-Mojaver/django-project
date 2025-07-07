from __future__ import annotations

from chat.models import Message, User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def message_list_partial(
    request: HttpRequest,
    user_id: int,
    other_user_id: int,
) -> HttpResponse | JsonResponse:
    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    other_user = User.objects.filter(id=other_user_id).first()
    if not other_user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    messages = Message.objects.filter(
        sender__in=[user, other_user], recipient__in=[user, other_user]
    ).order_by("created_at")

    context = {
        "messages": messages,
        "user_fullname": user.fullname,
        "other_user_fullname": other_user.fullname,
        "user_id": user.id,
    }

    return render(request, "partials/message_list.html", context)
