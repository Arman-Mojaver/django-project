import os
import sys
from pathlib import Path

import django
import pytest
from django.core.management import call_command

sys.path.append(Path(__file__).resolve().parent.parent.parent.as_posix())

os.environ["ENVIRONMENT"] = "testing"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jbl_chat.jbl_chat.settings")

from config import config as project_config

if not project_config.is_testing():
    err = f"Invalid testing environment: {project_config}"


django.setup()


@pytest.fixture(scope="session", autouse=True)
def django_cleanup_and_migrate():
    call_command("flush", interactive=False)
    call_command("migrate", interactive=False)


@pytest.fixture(autouse=True)
def flush_db_before_test():
    call_command("flush", interactive=False)
