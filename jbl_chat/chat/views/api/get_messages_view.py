from __future__ import annotations

from chat.models import Message, User
from chat.serializers import MessageSerializer
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def get_messages(
    _request: HttpRequest,
    sender_id: int,
    recipient_id: int,
) -> JsonResponse:
    sender_user = User.objects.filter(id=sender_id).first()
    if not sender_user:
        return JsonResponse(
            {"error": f"Sender user does not exist. ID: {sender_id}"},
            status=404,
        )

    recipient_user = User.objects.filter(id=recipient_id).first()
    if not recipient_user:
        return JsonResponse(
            {"error": f"Recipient user does not exist. ID: {recipient_id}"},
            status=404,
        )

    messages = Message.objects.filter(
        Q(sender_id=sender_id, recipient_id=recipient_id)
        | Q(sender_id=recipient_id, recipient_id=sender_id)
    ).order_by("created_at")

    serialized_messages = [MessageSerializer(message).data for message in messages]
    return JsonResponse({"data": serialized_messages})
