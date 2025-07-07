from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from chat.controllers.get_two_users_controller import GetTwoUsersController
from chat.errors import NotFoundError, SameUserError
from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def messages(
    request: HttpRequest,
    user_id: int,
    other_user_id: int,
) -> HttpResponse:
    controller = GetTwoUsersController(user_id=user_id, other_user_id=other_user_id)
    try:
        user, other_user = controller.run()
    except NotFoundError as e:
        error = {"error": str(e)}
        return render(request, "error.html", error, status=HTTPStatus.NOT_FOUND)
    except SameUserError as e:
        error = {"error": str(e)}
        return render(
            request,
            "error.html",
            error,
            status=HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    context = {
        "user_id": user.id,
        "user_fullname": user.fullname,
        "other_user_id": other_user.id,
        "other_user_fullname": other_user.fullname,
    }
    return render(request, "messages.html", context)
