from env import env
from database import Database, USER_CITIES
from utils.progress import header, success, info


def main():
    header("Database Sharding Benchmark")

    database = Database(
        maindb_url=env.MAINDB_URL, shard_urls=env.SHARD_URLS, cities=USER_CITIES
    )

    database.test_connection()

    num_users = env.MAX_GEN_USERS
    database.generate_data(num_users, batch_size=10000)

    database.benchmark(iterations=10)

    header("Benchmark Complete")
    info("Check the results above to see which approach performs better")
    success("Done!")


if __name__ == "__main__":
    main()
