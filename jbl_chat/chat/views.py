from django.http import HttpRequest, JsonResponse


def index(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"message": "Server Working!"})
