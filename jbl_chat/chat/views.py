import json

from chat.models import Message, User
from chat.serializers import MessageSerializer, UserSerializer
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST


def index(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"message": "Server Working!"})


@require_GET
def get_users(_request: HttpRequest, user_id: int) -> JsonResponse:
    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"})

    users = User.objects.exclude(id=user_id).all()

    serialized_users = [UserSerializer(user).data for user in users]
    return JsonResponse({"data": serialized_users})


@require_GET
def get_messages(_request: HttpRequest, sender_id: int, recipient_id: int):  # noqa: ANN201
    sender_user = User.objects.filter(id=sender_id).first()
    if not sender_user:
        return JsonResponse({"error": f"Sender user does not exist. ID: {sender_id}"})

    recipient_user = User.objects.filter(id=recipient_id).first()
    if not recipient_user:
        return JsonResponse(
            {"error": f"Recipient user does not exist. ID: {recipient_id}"}
        )

    messages = Message.objects.filter(
        Q(sender_id=sender_id, recipient_id=recipient_id)
        | Q(sender_id=recipient_id, recipient_id=sender_id)
    ).order_by("created_at")

    serialized_messages = [MessageSerializer(message).data for message in messages]
    return JsonResponse({"data": serialized_messages})


@require_POST
def create_message(request: HttpRequest, sender_id: int, recipient_id: int):  # noqa: ANN201
    sender_user = User.objects.filter(id=sender_id).first()
    if not sender_user:
        return JsonResponse({"error": f"Sender user does not exist. ID: {sender_id}"})

    recipient_user = User.objects.filter(id=recipient_id).first()
    if not recipient_user:
        return JsonResponse(
            {"error": f"Recipient user does not exist. ID: {recipient_id}"}
        )

    data = json.loads(request.body)
    content = data.get("content")

    if content is None:
        return JsonResponse({"error": f"Invalid content: {content}"})

    message = Message.objects.create(
        content=content,
        sender_id=sender_id,
        recipient_id=recipient_id,
    )
    serialized_message = MessageSerializer(message).data

    return JsonResponse({"data": serialized_message})
