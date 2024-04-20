from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings class for managing application settings.

    Attributes:
        sqlalchemy_database_url (str): The URL for connecting to the SQLAlchemy database.
        secret_key (str): The secret key used for JWT token encryption.
        algorithm (str): The algorithm used for JWT token encryption.
        mail_username (str): The username for the email server.
        mail_password (str): The password for the email server.
        mail_from (str): The email address from which emails will be sent.
        mail_port (int): The port number for the email server.
        mail_server (str): The SMTP server for sending emails.
        redis_host (str): The hostname of the Redis server (default is 'localhost').
        redis_port (int): The port number of the Redis server (default is 6379).
        postgres_db (str): The name of the PostgreSQL database.
        postgres_user (str): The username for accessing the PostgreSQL database.
        postgres_password (str): The password for accessing the PostgreSQL database.
        postgres_port (int): The port number for the PostgreSQL database.
        cloudinary_name (str): The cloudinary account name.
        cloudinary_api_key (str): The API key for accessing the cloudinary service.
        cloudinary_api_secret (str): The API secret for accessing the cloudinary service.
        origins_url (str): The allowed origins for CORS (Cross-Origin Resource Sharing).

    """
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: int
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str
    origins_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

