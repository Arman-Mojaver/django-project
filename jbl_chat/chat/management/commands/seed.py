from __future__ import annotations

import random
import time

from chat.models import Message, User
from django.core.management.base import BaseCommand
from faker import Faker

fake = Faker()


def _create_users(count: int) -> list[User]:
    users = []
    for _ in range(count):
        user = User.objects.create(
            fullname=fake.name(),
            email=fake.unique.email(),
        )
        users.append(user)

    return users


def _create_messages(users: list[User], count: int) -> list[Message]:
    messages = []
    for _ in range(count):
        sender, recipient = random.sample(users, 2)
        message = Message.objects.create(
            content=fake.text(max_nb_chars=100), sender=sender, recipient=recipient
        )
        messages.append(message)

        # Add a time gap in the creation time so the order can easily be seen in the UI
        time.sleep(0.2)

    return messages


class Command(BaseCommand):
    help = "Seed the database with test users and messages"

    def handle(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003, ARG002
        self.stdout.write(self.style.NOTICE("Seeding data..."))

        users_with_messages = _create_users(count=5)
        users_without_messages = _create_users(count=5)
        messages = _create_messages(users=users_with_messages, count=50)

        users_count = len(users_with_messages) + len(users_without_messages)
        self.stdout.write(self.style.SUCCESS(f"Created {users_count} users."))
        self.stdout.write(self.style.SUCCESS(f"Created {len(messages)} messages."))
        self.stdout.write(self.style.SUCCESS("Seeding completed!"))
