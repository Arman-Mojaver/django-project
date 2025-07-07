from __future__ import annotations

from chat.controllers.get_user_controller import GetUserController
from chat.errors import NotFoundError
from chat.models import User


class GetOtherUsersController:
    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id

    def _validate_user_exists(self) -> None:
        controller = GetUserController(user_id=self.user_id)
        try:
            controller.run()
        except NotFoundError:  # noqa: TRY203
            raise

    def run(self) -> list[User]:
        self._validate_user_exists()
        return User.objects.exclude(id=self.user_id).all()
