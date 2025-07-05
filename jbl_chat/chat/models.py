from django.db import models


class User(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.fullname
