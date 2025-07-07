from __future__ import annotations

from http import HTTPStatus

from chat.controllers.get_other_users_controller import GetOtherUsersController
from chat.errors import NotFoundError
from chat.serializers import UserSerializer
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def get_users(_request: HttpRequest, user_id: int) -> JsonResponse:
    controller = GetOtherUsersController(user_id=user_id)
    try:
        users = controller.run()
    except NotFoundError as e:
        return JsonResponse({"error": str(e)}, status=HTTPStatus.NOT_FOUND)

    serialized_users = [UserSerializer(user).data for user in users]
    return JsonResponse({"data": serialized_users})
