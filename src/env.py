import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class EnvSchema:
    DEBUG: bool

    MAX_GEN_USERS: int
    AUTO_GENERATE: bool

    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str

    MAIN_DB_PORT: int
    MAIN_DB_NAME: str

    ODD_USER_ID_DB_PORT: int
    ODD_USER_ID_DB_NAME: str

    EVEN_USER_ID_DB_PORT: int
    EVEN_USER_ID_DB_NAME: str


env = EnvSchema(
    DEBUG=os.getenv("DEBUG"),
    MAX_GEN_USERS=os.getenv("MAX_GEN_USERS"),
    AUTO_GENERATE=os.getenv("AUTO_GENERATE"),
    DB_HOST=os.getenv("DB_HOST"),
    DB_USER=os.getenv("DB_USER"),
    DB_PASSWORD=os.getenv("DB_PASSWORD"),
    MAIN_DB_PORT=int(os.getenv("MAIN_DB_PORT")),
    MAIN_DB_NAME=os.getenv("MAIN_DB_NAME"),
    ODD_USER_ID_DB_PORT=int(os.getenv("ODD_USER_ID_DB_PORT")),
    ODD_USER_ID_DB_NAME=os.getenv("ODD_USER_ID_DB_NAME"),
    EVEN_USER_ID_DB_PORT=int(os.getenv("EVEN_USER_ID_DB_PORT")),
    EVEN_USER_ID_DB_NAME=os.getenv("EVEN_USER_ID_DB_NAME"),
)
