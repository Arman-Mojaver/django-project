from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from chat.controllers.get_user_controller import GetUserController
from chat.errors import NotFoundError
from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def users(request: HttpRequest, user_id: int) -> HttpResponse:
    controller = GetUserController(user_id=user_id)
    try:
        user = controller.run()
    except NotFoundError as e:
        error = {"error": str(e)}
        return render(request, "error.html", error, status=HTTPStatus.NOT_FOUND)

    context = {"user_id": user.id, "user_fullname": user.fullname}
    return render(request, "users.html", context)
