from config.base import BaseConfig


class TestingConfig(BaseConfig):
    POSTGRES_HOST = "db-testing"
    POSTGRES_PORT = 54321
    POSTGRES_USER = "postgres"
    POSTGRES_PASS = "postgres"
    POSTGRES_DB = "db-testing"
