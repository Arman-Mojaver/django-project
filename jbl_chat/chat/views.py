from __future__ import annotations

import json

from chat.models import Message, User
from chat.serializers import MessageSerializer, UserSerializer
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST


def index(_request: HttpRequest) -> JsonResponse:
    return redirect("/login/")


@require_GET
def get_users(_request: HttpRequest, user_id: int) -> JsonResponse:
    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    users = User.objects.exclude(id=user_id).all()

    serialized_users = [UserSerializer(user).data for user in users]
    return JsonResponse({"data": serialized_users})


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
            status=404,
        )

    recipient_user = User.objects.filter(id=recipient_id).first()
    if not recipient_user:
        return JsonResponse(
            {"error": f"Recipient user does not exist. ID: {recipient_id}"},
            status=404,
        )

    data = json.loads(request.body)
    content = data.get("content")

    if content is None:
        return JsonResponse({"error": f"Invalid content: {content}"}, status=400)

    message = Message.objects.create(
        content=content,
        sender_id=sender_id,
        recipient_id=recipient_id,
    )
    serialized_message = MessageSerializer(message).data

    return JsonResponse({"data": serialized_message})


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login.html")


def users(request: HttpRequest, user_id: int) -> HttpResponse | JsonResponse:
    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    context = {"user_id": user.id, "user_fullname": user.fullname}
    return render(request, "users.html", context)


def messages(
    request: HttpRequest,
    user_id: int,
    other_user_id: int,
) -> HttpResponse | JsonResponse:
    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    other_user = User.objects.filter(id=other_user_id).first()
    if not other_user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    if user_id == other_user_id:
        return JsonResponse(
            {"error": "Invalid path: Users can not be the same"},
            status=422,
        )
    context = {
        "user_id": user.id,
        "user_fullname": user.fullname,
        "other_user_id": other_user.id,
        "other_user_fullname": other_user.fullname,
    }
    return render(request, "messages.html", context)


def message_list_partial(
    request: HttpRequest,
    user_id: int,
    other_user_id: int,
) -> HttpResponse | JsonResponse:
    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    other_user = User.objects.filter(id=other_user_id).first()
    if not other_user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    messages = Message.objects.filter(
        sender__in=[user, other_user], recipient__in=[user, other_user]
    ).order_by("created_at")

    context = {
        "messages": messages,
        "user_fullname": user.fullname,
        "other_user_fullname": other_user.fullname,
        "user_id": user.id,
    }

    return render(request, "partials/message_list.html", context)


@require_POST
def message_create_partial(
    request: HttpRequest,
    user_id: int,
    other_user_id: int,
) -> HttpResponse | JsonResponse:
    content = request.POST.get("content")
    if content is None:
        return JsonResponse({"error": f"Invalid content: {content}"}, status=400)

    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    other_user = User.objects.filter(id=other_user_id).first()
    if not other_user:
        return JsonResponse({"error": f"User does not exist. ID: {user_id}"}, status=404)

    message = Message.objects.create(sender=user, recipient=other_user, content=content)

    context = {
        "message": message,
        "user_fullname": user.fullname,
        "other_user_fullname": other_user.fullname,
        "user_id": user.id,
    }

    return render(request, "partials/message_row.html", context)
