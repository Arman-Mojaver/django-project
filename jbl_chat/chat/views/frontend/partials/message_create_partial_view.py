from __future__ import annotations

from http import HTTPStatus

from chat.controllers.get_two_users_controller import GetTwoUsersController
from chat.errors import NotFoundError, SameUserError
from chat.models import Message
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

    message = Message.objects.create(sender=user, recipient=other_user, content=content)

    context = {
        "message": message,
        "user_fullname": user.fullname,
        "other_user_fullname": other_user.fullname,
        "user_id": user.id,
    }

    return render(request, "partials/message_row.html", context)
