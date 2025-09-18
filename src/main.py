from env import env
from database import database

if __name__ == "__main__":
    if env.AUTO_GENERATE:
        database.test_connection()
        database.generate_data(num_users=env.MAX_GEN_USERS)
