from django.contrib import admin

from .models import Message, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname", "email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "sender", "recipient", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content",)
