from __future__ import annotations

from chat.errors import NotFoundError, SameUserError
from chat.models import User


class GetTwoUsersController:
    def __init__(self, user_id: int, other_user_id: int) -> None:
        self.user_id: int = user_id
        self.other_user_id: int = other_user_id

        self.user: User | None = None
        self.other_user: User | None = None

    def _validate_users_are_different(self):
        if self.user_id == self.other_user_id:
            err = f"Users can not be the same: {self.user_id}, {self.other_user_id}"
            raise SameUserError(err)

    @staticmethod
    def _get_user(user_id: int) -> User:
        return User.objects.filter(id=user_id).first()

    def _validate_users_exist(self) -> None:
        if not self.user:
            err = f"User does not exist. ID: {self.user_id}"
            raise NotFoundError(err)

        if not self.other_user:
            err = f"User does not exist. ID: {self.other_user_id}"
            raise NotFoundError(err)

    def run(self) -> list[User]:
        self._validate_users_are_different()
        self.user = self._get_user(user_id=self.user_id)
        self.other_user = self._get_user(user_id=self.other_user_id)
        self._validate_users_exist()
        return [self.user, self.other_user]
