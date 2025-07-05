from config.base import BaseConfig


class ProductionConfig(BaseConfig):
    POSTGRES_HOST = "db-production"
    POSTGRES_PORT = 5432
    POSTGRES_USER = "postgres"
    POSTGRES_PASS = "postgres"
    POSTGRES_DB = "db-production"
