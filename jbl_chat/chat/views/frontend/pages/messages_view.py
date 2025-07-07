from __future__ import annotations

from http import HTTPStatus

from chat.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def messages(
    request: HttpRequest,
    user_id: int,
    other_user_id: int,
) -> HttpResponse | JsonResponse:
    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse(
            {"error": f"User does not exist. ID: {user_id}"},
            status=HTTPStatus.NOT_FOUND,
        )

    other_user = User.objects.filter(id=other_user_id).first()
    if not other_user:
        return JsonResponse(
            {"error": f"User does not exist. ID: {user_id}"},
            status=HTTPStatus.NOT_FOUND,
        )

    if user_id == other_user_id:
        return JsonResponse(
            {"error": "Invalid path: Users can not be the same"},
            status=HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    context = {
        "user_id": user.id,
        "user_fullname": user.fullname,
        "other_user_id": other_user.id,
        "other_user_fullname": other_user.fullname,
    }
    return render(request, "messages.html", context)
