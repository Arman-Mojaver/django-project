from chat.models import User
from chat.serializers import UserSerializer
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET


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
