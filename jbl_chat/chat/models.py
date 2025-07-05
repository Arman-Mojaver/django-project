from django.db import models


class User(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.fullname


class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(
        User,
        related_name="sent_messages",
        on_delete=models.CASCADE,
    )
    recipient = models.ForeignKey(
        User,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.recipient}"
