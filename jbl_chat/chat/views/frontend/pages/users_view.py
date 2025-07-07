from __future__ import annotations

from http import HTTPStatus

from chat.controllers.get_user_controller import GetUserController
from chat.errors import NotFoundError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def users(request: HttpRequest, user_id: int) -> HttpResponse | JsonResponse:
    controller = GetUserController(user_id=user_id)
    try:
        user = controller.run()
    except NotFoundError as e:
        return JsonResponse({"error": str(e)}, status=HTTPStatus.NOT_FOUND)

    context = {"user_id": user.id, "user_fullname": user.fullname}
    return render(request, "users.html", context)
