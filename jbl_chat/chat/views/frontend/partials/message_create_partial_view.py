from __future__ import annotations

from http import HTTPStatus

from chat.models import Message, User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST


@require_POST
def message_create_partial(
    request: HttpRequest,
    user_id: int,
    other_user_id: int,
) -> HttpResponse | JsonResponse:
    content = request.POST.get("content")
    if content is None:
        return JsonResponse(
            {"error": f"Invalid content: {content}"},
            status=HTTPStatus.BAD_REQUEST,
        )

    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse(
            {"error": f"User does not exist. ID: {user_id}"},
            status=HTTPStatus.NOT_FOUND,
        )

    other_user = User.objects.filter(id=other_user_id).first()
    if not other_user:
        return JsonResponse(
            {"error": f"User does not exist. ID: {other_user_id}"},
            status=HTTPStatus.NOT_FOUND,
        )

    message = Message.objects.create(sender=user, recipient=other_user, content=content)

    context = {
        "message": message,
        "user_fullname": user.fullname,
        "other_user_fullname": other_user.fullname,
        "user_id": user.id,
    }

    return render(request, "partials/message_row.html", context)
