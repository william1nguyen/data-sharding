from env import env
from dataclasses import dataclass
import psycopg2


@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str

    @property
    def url(self) -> str:
        """Generate SQLAlchemy database URL."""
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

    def connect(self, config):
        try:
            return psycopg2.connect(config)
        except Exception as e:
            print(f"Failed to connect database {e}")

    def test_connection(self):
        print("Test connection...")

        databases = [
            ("Main", self.main_db.url),
            ("Odd User ID", self.odd_user_id_db.url),
            ("Even User ID", self.even_user_id_db.url),
        ]

        for name, config in databases:
            conn = self.connect(config=config)

            if conn:
                print(f"{name} connected")
                conn.close()
            else:
                print(f"{name} connected failed")

    def clear_data(self):
        pass

    def generate_data(self, num_users=1000):
        print(f"Generating {num_users} users...")


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


database.test_connection()
