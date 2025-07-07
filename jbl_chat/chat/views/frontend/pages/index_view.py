from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import redirect

if TYPE_CHECKING:
    from django.http import HttpRequest, JsonResponse


def index(_request: HttpRequest) -> JsonResponse:
    return redirect("/login/")
