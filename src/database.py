import time
import random
from env import env
from dataclasses import dataclass
import psycopg2
from faker import Faker
from models import User
from utils.progress import (
    progress_bar,
    info,
    success,
    error,
    warn,
    header,
    inline_success,
    inline_error,
)


@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


USER_CITIES = ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hai Phong", "Can Tho"]


class Database:
    def __init__(
        self,
        main_db: DatabaseConfig,
        odd_user_id_db: DatabaseConfig,
        even_user_id_db: DatabaseConfig,
        cities,
    ):
        self.main_db = main_db
        self.odd_user_id_db = odd_user_id_db
        self.even_user_id_db = even_user_id_db
        self.cities = cities
        self.fake = Faker("vi_VN")

    def connect(self, config):
        try:
            return psycopg2.connect(config)
        except Exception as e:
            error(f"DB connection failed: {e}")

    def test_connection(self):
        info("Testing connections...")
        dbs = [
            ("Main", self.main_db.url),
            ("Odd", self.odd_user_id_db.url),
            ("Even", self.even_user_id_db.url),
        ]
        for name, config in dbs:
            conn = self.connect(config)
            if conn:
                inline_success(name)
                conn.close()
            else:
                inline_error(name)
        print()

    def clear_data(self):
        info("Clearing existing data...")
        configs = [
            ("Main", self.main_db.url),
            ("Odd", self.odd_user_id_db.url),
            ("Even", self.even_user_id_db.url),
        ]

        for name, config in configs:
            conn = self.connect(config)
            if conn:
                try:
                    conn.cursor().execute("TRUNCATE users RESTART IDENTITY")
                    conn.commit()
                    conn.close()
                    inline_success(name)
                except Exception as e:
                    inline_error(f"{name} ({e})")
        print()

    def generate_user(self, id: int) -> User:
        return User(
            id=id,
            name=self.fake.name(),
            email=f"user{id}@{self.fake.domain_name()}",
            age=random.randint(18, 70),
            city=random.choice(self.cities),
        )

    def generate_data(self, num_users=1000):
        header(f"Generating {num_users:,} users")
        self.clear_data()

        users = [self.generate_user(id) for id in range(1, num_users + 1)]
        odd_users = [u for u in users if u.id % 2 == 1]
        even_users = [u for u in users if u.id % 2 == 0]

        info("Inserting data...")
        self._insert(self.main_db, [u.to_tuple() for u in users], "Main")
        self._insert(self.even_user_id_db, [u.to_tuple() for u in even_users], "Even")
        self._insert(self.odd_user_id_db, [u.to_tuple() for u in odd_users], "Odd")

        success(f"Generated {num_users:,} users successfully!")

    def _insert(self, config, data, db_name, batch_size=1000):
        conn = self.connect(config.url)
        if not conn:
            return

        try:
            cursor = conn.cursor()
            total = len(data)
            start = time.time()

            for i in range(0, total, batch_size):
                batch = data[i : i + batch_size]
                cursor.executemany(
                    "INSERT INTO users (user_id, name, email, age, city, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
                    batch,
                )
                progress_bar(min(i + batch_size, total), total, db_name, start)

            conn.commit()
            conn.close()
        except Exception as e:
            error(f"{db_name} insert failed: {e}")


database = Database(
    main_db=DatabaseConfig(
        host=env.DB_HOST,
        user=env.DB_USER,
        password=env.DB_PASSWORD,
        name=env.MAIN_DB_NAME,
        port=env.MAIN_DB_PORT,
    ),
    odd_user_id_db=DatabaseConfig(
        host=env.DB_HOST,
        user=env.DB_USER,
        password=env.DB_PASSWORD,
        name=env.ODD_USER_ID_DB_NAME,
        port=env.ODD_USER_ID_DB_PORT,
    ),
    even_user_id_db=DatabaseConfig(
        host=env.DB_HOST,
        user=env.DB_USER,
        password=env.DB_PASSWORD,
        name=env.EVEN_USER_ID_DB_NAME,
        port=env.EVEN_USER_ID_DB_PORT,
    ),
    cities=USER_CITIES,
)
