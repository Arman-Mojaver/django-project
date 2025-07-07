from __future__ import annotations

from http import HTTPStatus

from chat.controllers.get_two_users_controller import GetTwoUsersController
from chat.errors import NotFoundError, SameUserError
from chat.models import Message
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def message_list_partial(
    request: HttpRequest,
    user_id: int,
    other_user_id: int,
) -> HttpResponse | JsonResponse:
    controller = GetTwoUsersController(
        user_id=user_id,
        other_user_id=other_user_id,
    )
    try:
        user, other_user = controller.run()
    except NotFoundError as e:
        return JsonResponse({"error": str(e)}, status=HTTPStatus.NOT_FOUND)
    except SameUserError as e:
        return JsonResponse({"error": str(e)}, status=HTTPStatus.UNPROCESSABLE_ENTITY)

    messages = Message.objects.filter(
        sender__in=[user, other_user],
        recipient__in=[user, other_user],
    ).order_by("created_at")

    context = {
        "messages": messages,
        "user_fullname": user.fullname,
        "other_user_fullname": other_user.fullname,
        "user_id": user.id,
    }

    return render(request, "partials/message_list.html", context)
