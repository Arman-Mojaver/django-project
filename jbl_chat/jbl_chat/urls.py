"""
jbl_chat URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/

Examples
--------
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from chat.views import (
    create_message,
    get_messages,
    get_users,
    index,
    login,
    message_create_partial,
    message_list_partial,
    messages,
    users,
)
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("api/users/<int:user_id>/", get_users),
    path("api/messages/<int:sender_id>/<int:recipient_id>/", get_messages),
    path("api/message/<int:sender_id>/<int:recipient_id>/", create_message),
    path("login/", login),
    path("users/<int:user_id>/", users),
    path("messages/<int:user_id>/<int:other_user_id>/", messages),
    path(
        "messages/partials/<int:user_id>/<int:other_user_id>/",
        message_list_partial,
        name="message_list_partial",
    ),
    path(
        "message/partials/<int:user_id>/<int:other_user_id>/",
        message_create_partial,
        name="message_create_partial",
    ),
]
