import time
import random
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from faker import Faker
from models import User
from utils.progress import (
    progress_bar,
    info,
    success,
    error,
    header,
    inline_success,
    inline_error,
)
from typing import List

USER_CITIES = ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hai Phong", "Can Tho"]


class Database:
    def __init__(self, maindb_url: str, shard_urls: List[str], cities=USER_CITIES):
        self.main_url = maindb_url
        self.shard_urls = shard_urls
        self.fake = Faker("vi_VN")
        self.cities = cities

    @contextmanager
    def get_connection(self, db_url):
        conn = None
        try:
            conn = psycopg2.connect(db_url)
            yield conn
        except Exception as e:
            error(f"Connection failed: {e}")
            yield None
        finally:
            if conn:
                conn.close()

    def test_connection(self):
        info("Testing connections...")
        with self.get_connection(self.main_url) as conn:
            inline_success("main") if conn else inline_error("main")

        for i, url in enumerate(self.shard_urls):
            with self.get_connection(url) as conn:
                inline_success(f"shard{i}") if conn else inline_error(f"shard{i}")
        print()

    def clear_data(self):
        info("Clearing data...")
        [
            self._clear_db(url, name)
            for url, name in [(self.main_url, "main")]
            + [(url, f"shard{i}") for i, url in enumerate(self.shard_urls)]
        ]
        print()

    def _clear_db(self, db_url, name):
        with self.get_connection(db_url) as conn:
            if conn:
                try:
                    conn.cursor().execute("TRUNCATE users RESTART IDENTITY")
                    conn.commit()
                    inline_success(name)
                except Exception as e:
                    inline_error(f"{name}({e})")

    def generate_data(self, num_users=1000, batch_size=1000):
        num_users = int(num_users)
        header(f"Generating {num_users} users")
        self.clear_data()

        info("Generating users to Main DB...")
        start_time = time.time()

        for start_id in range(1, num_users + 1, batch_size):
            end_id = min(start_id + batch_size - 1, num_users)
            users = [
                self._generate_user(uid).to_tuple()
                for uid in range(start_id, end_id + 1)
            ]
            self._insert_users(self.main_url, users)
            progress_bar(end_id, num_users, "Generating", start_time)

        print()
        self._migrate_to_shards()
        success(f"Generated and distributed {num_users} users")

    def _generate_user(self, user_id):
        return User(
            user_id=user_id,
            name=self.fake.name(),
            email=f"user{user_id}@{self.fake.domain_name()}",
            age=random.randint(18, 70),
            city=random.choice(self.cities),
        )

    def _insert_users(self, db_url, users):
        with self.get_connection(db_url) as conn:
            if conn and users:
                psycopg2.extras.execute_values(
                    conn.cursor(),
                    "INSERT INTO users (user_id, name, email, age, city, created_at) VALUES %s",
                    users,
                    page_size=5000,
                )
                conn.commit()

    def _migrate_to_shards(self):
        info("Migrating data to shards...")

        with self.get_connection(self.main_url) as conn:
            if not conn:
                return
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, name, email, age, city, created_at FROM users ORDER BY user_id"
            )
            all_users = cursor.fetchall()

        shard_data = [[] for _ in self.shard_urls]
        [shard_data[user[0] % len(self.shard_urls)].append(user) for user in all_users]

        for i, (url, users) in enumerate(zip(self.shard_urls, shard_data)):
            if users:
                info(f"Migrating to Shard{i}...")
                start_time = time.time()
                for j in range(0, len(users), 1000):
                    batch = users[j : j + 1000]
                    self._insert_users(url, batch)
                    progress_bar(
                        min(j + 1000, len(users)), len(users), f"Shard{i}", start_time
                    )
                print()

    def benchmark(self, iterations=5):
        header("Benchmark: Main vs Sharded")
        tests = [
            ("Point", "SELECT * FROM users WHERE user_id = %s"),
            ("Range", "SELECT * FROM users WHERE user_id BETWEEN %s AND %s"),
            ("Count", "SELECT COUNT(*) FROM users WHERE age > 30"),
            ("City", "SELECT COUNT(*) FROM users WHERE city = 'Hanoi'"),
        ]

        for test_name, sql in tests:
            info(f"Testing {test_name}")
            main_time = self._benchmark_db(sql, iterations, [self.main_url])
            shard_time = self._benchmark_db(sql, iterations, self.shard_urls, True)
            winner = "Main" if main_time < shard_time else "Shard"
            faster, slower = (
                (main_time, shard_time)
                if main_time < shard_time
                else (shard_time, main_time)
            )
            success(f"{test_name}: {winner} wins ({faster:.1f}ms vs {slower:.1f}ms)")

    def _benchmark_db(self, sql, iterations, urls, is_shard=False):
        start = time.time()
        for _ in range(iterations):
            if is_shard and "user_id =" in sql:
                uid = random.randint(1, 1000)
                self._execute_query(urls[uid % len(urls)], sql, (uid,))
            elif is_shard and "BETWEEN" in sql:
                params = (random.randint(1, 500), random.randint(501, 1000))
                [self._execute_query(url, sql, params) for url in urls]
            else:
                params = self._get_params(sql)
                [self._execute_query(url, sql, params) for url in urls]
        return (time.time() - start) / iterations * 1000

    def _get_params(self, sql):
        if "user_id =" in sql:
            return (random.randint(1, 1000),)
        elif "BETWEEN" in sql:
            return (random.randint(1, 500), random.randint(501, 1000))
        return None

    def _execute_query(self, db_url, sql, params=None):
        try:
            with self.get_connection(db_url) as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute(sql, params)
                    return cursor.fetchall()
        except:
            pass
        return []
