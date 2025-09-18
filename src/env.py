import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List

load_dotenv()


@dataclass
class Environment:
    MAINDB_URL: str
    SHARD_URLS: List[str]
    MAX_GEN_USERS: int


def load_environment():
    maindb_url = os.getenv("MAINDB_URL")
    shard_urls_string = os.getenv("SHARD_URLS", "")
    shard_urls = [url.strip() for url in shard_urls_string.split(",")]
    max_gen_users = int(os.getenv("MAX_GEN_USERS", 1000))

    return Environment(
        MAINDB_URL=maindb_url, SHARD_URLS=shard_urls, MAX_GEN_USERS=max_gen_users
    )


env = load_environment()
