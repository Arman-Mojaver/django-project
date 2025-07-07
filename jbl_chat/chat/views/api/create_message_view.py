from __future__ import annotations

import json
from http import HTTPStatus

from chat.models import Message, User
from chat.serializers import MessageSerializer
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST


@require_POST
def create_message(
    request: HttpRequest,
    sender_id: int,
    recipient_id: int,
) -> JsonResponse:
    sender_user = User.objects.filter(id=sender_id).first()
    if not sender_user:
        return JsonResponse(
            {"error": f"Sender user does not exist. ID: {sender_id}"},
            status=HTTPStatus.NOT_FOUND,
        )

    recipient_user = User.objects.filter(id=recipient_id).first()
    if not recipient_user:
        return JsonResponse(
            {"error": f"Recipient user does not exist. ID: {recipient_id}"},
            status=HTTPStatus.NOT_FOUND,
        )

    data = json.loads(request.body)
    content = data.get("content")

    if content is None:
        return JsonResponse(
            {"error": f"Invalid content: {content}"},
            status=HTTPStatus.BAD_REQUEST,
        )

    message = Message.objects.create(
        content=content,
        sender_id=sender_id,
        recipient_id=recipient_id,
    )
    serialized_message = MessageSerializer(message).data

    return JsonResponse({"data": serialized_message})
