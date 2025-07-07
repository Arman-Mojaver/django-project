from chat.errors import NotFoundError
from chat.models import User


class GetUserController:
    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id

        self.user: User | None = None

    def _get_user(self) -> User:
        return User.objects.filter(id=self.user_id).first()

    def _validate_user_exists(self) -> None:
        if not self.user:
            err = f"User does not exist. ID: {self.user_id}"
            raise NotFoundError(err)

    def run(self) -> User:
        self.user = self._get_user()
        self._validate_user_exists()
        return self.user
